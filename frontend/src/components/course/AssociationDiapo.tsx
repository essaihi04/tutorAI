import { useEffect, useMemo, useRef, useState, type PointerEvent as ReactPointerEvent } from 'react';
import { createPortal } from 'react-dom';
import { Formule } from './Formule';
import type { AssociationQuestion, RetourPaire } from './types';

/**
 * Une question d'association posée sur une diapositive (19 novembre 2026, demande de l'utilisateur : « pour les
 * questions d'association, ne pas les transformer en QCM ; les mettre en association avec un feedback à chaque réponse,
 * correcte ou fausse »).
 *
 * L'élève relie lui-même : il GLISSE un élément d'une colonne sur un élément de l'autre, ou il TOUCHE l'un puis
 * l'autre (dans les deux sens). Chaque paire formée reçoit tout de suite son retour, écrit et dit :
 *  - juste : la paire reste reliée (même couleur des deux côtés), le retour dit pourquoi ;
 *  - fausse : les deux éléments rougissent un instant puis se délient ; le retour dit ce qui ne va pas et donne un
 *    indice, jamais la bonne lettre. Après `essais` erreurs sur le même élément de gauche (2 par défaut), la bonne
 *    paire est posée pour lui, avec son retour (elle compte comme donnée, pas trouvée).
 * Toutes les paires posées : la ligne des couples comme le barème les attend, « (1 ; c) (2 ; e) … », et le bilan
 * (`bilan`) partent à `onFin`, qui les montre et les dit comme la réaction d'une question ordinaire.
 */

export type FinAssociation = {
  /** toutes les paires trouvées par l'élève (aucune donnée) */
  correct: boolean;
  /** 1 : sans aucune erreur ; 2 : avec des erreurs */
  tentative: number;
  /** « (1 ; c) (2 ; e) … » puis le texte du bilan */
  ecrit: string;
  /** la réponse de l'élève, pour le suivi des acquis */
  reponse: string;
};

type Etat = { poses: Record<string, string>; erreurs: Record<string, number>; donnees: string[] };
type Prise = { cote: 'g' | 'd'; id: string; x: number; y: number; glisse: boolean };

/** Vrai tant que l'écran répond à la requête média (écran bas : les colonnes se resserrent ; téléphone en paysage). */
function useEcran(requete: string) {
  const [oui, setOui] = useState(() => typeof window !== 'undefined' && window.matchMedia(requete).matches);
  useEffect(() => {
    const m = window.matchMedia(requete), suivre = () => setOui(m.matches);
    suivre();
    m.addEventListener('change', suivre);
    return () => m.removeEventListener('change', suivre);
  }, [requete]);
  return oui;
}

const COULEURS = ['#fde68a', '#a5f3fc', '#f9a8d4', '#bbf7d0', '#c4b5fd', '#fdba74'];
const FAUTE_MS = 1600;

/** La ligne des couples comme le barème les attend : « (1 ; c) (2 ; e) (3 ; b) (4 ; a) ». */
export function ligneDesCouples(a: AssociationQuestion): string {
  return a.gauche.map(g => `(${g.id} ; ${a.couples[g.id] ?? '?'})`).join(' ');
}

/** Le retour d'une paire : le sien, sinon celui de son élément de gauche (`g-*`) si elle est fausse, sinon un mot simple. */
export function retourDe(a: AssociationQuestion, g: string, d: string): RetourPaire & { juste: boolean } {
  const juste = a.couples[g] === d;
  const r = a.retours?.[`${g}-${d}`] ?? (juste ? undefined : a.retours?.[`${g}-*`]);
  if (r) return { ...r, juste };
  return juste ? { juste, texte: `Juste : (${g} ; ${d}).` } : { juste, texte: `Pas encore : ${d} ne va pas avec ${g}. Regarde de nouveau, puis réessaie.` };
}

export default function AssociationDiapo({ a, memoire, fini, compact = false, actif = true, onPaire, onFin }: {
  a: AssociationQuestion;
  /** clé de l'état gardé pour l'élève (localStorage) */
  memoire: string;
  /** la question est close (bilan donné) : plus rien ne se relie */
  fini: boolean;
  compact?: boolean;
  actif?: boolean;
  /** une paire vient d'être formée : la voix dit son retour (piste préparée `audio`, sinon `dit`) ; renvoie la promesse de la voix.
   *  `apresVoix` : attendre que la voix en cours ait fini (la bonne paire posée après le retour d'une erreur). */
  onPaire: (r: RetourPaire & { juste: boolean }, g: string, d: string, apresVoix?: boolean) => Promise<unknown> | void;
  /** toutes les paires sont posées */
  onFin: (f: FinAssociation, voix: Promise<unknown>) => void;
}) {
  const cle = `${memoire}:association`;
  const [etat, setEtat] = useState<Etat>(() => {
    try { const e = JSON.parse(localStorage.getItem(cle) || 'null') as Etat | null; if (e?.poses) return { poses: e.poses, erreurs: e.erreurs || {}, donnees: e.donnees || [] }; } catch { /* sans mémoire locale */ }
    return { poses: {}, erreurs: {}, donnees: [] };
  });
  useEffect(() => { try { localStorage.setItem(cle, JSON.stringify(etat)); } catch { /* sans mémoire locale */ } }, [cle, etat]);
  const essais = Math.max(1, a.essais ?? 2);

  // La colonne de droite battue une fois (les étiquettes restent : « c- … »), jamais déjà dans l'ordre du sujet.
  const droite = useMemo(() => {
    const d = [...a.droite];
    if (a.melanger === false || d.length < 2) return d;
    for (let k = d.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [d[k], d[j]] = [d[j], d[k]]; }
    if (d.every((x, k) => x.id === a.droite[k].id)) d.push(d.shift()!);
    return d;
  }, [a]);

  const [choisi, setChoisi] = useState<{ cote: 'g' | 'd'; id: string } | null>(null);
  const [faute, setFaute] = useState<{ g: string; d: string } | null>(null);
  const [dernier, setDernier] = useState<(RetourPaire & { juste: boolean; donnee?: boolean }) | null>(null);
  const [prise, setPrise] = useState<Prise | null>(null);
  const priseRef = useRef<Prise | null>(null);
  const voix = useRef<Promise<unknown>>(Promise.resolve());
  const finEnvoyee = useRef(false);

  const couleurDe = (g: string) => COULEURS[a.gauche.findIndex(x => x.id === g) % COULEURS.length];
  const gPour = (d: string) => Object.entries(etat.poses).find(([, v]) => v === d)?.[0];
  const toutPose = a.gauche.every(g => etat.poses[g.id]);

  // Toutes les paires posées : le bilan, après le retour de la dernière paire.
  useEffect(() => {
    if (!toutPose || fini || finEnvoyee.current) return;
    finEnvoyee.current = true;
    const nErreurs = Object.values(etat.erreurs).reduce((s, n) => s + n, 0);
    const ecrit = [ligneDesCouples(a), a.bilan?.texte].filter(Boolean).join(' — ');
    const reponse = a.gauche.map(g => `(${g.id} ; ${etat.poses[g.id]})${etat.donnees.includes(g.id) ? ' donné' : ''}`).join(' ')
      + (nErreurs ? ` ; erreurs : ${Object.entries(etat.erreurs).filter(([, n]) => n).map(([g, n]) => `${g}×${n}`).join(', ')}` : '');
    onFin({ correct: etat.donnees.length === 0, tentative: nErreurs ? 2 : 1, ecrit, reponse }, voix.current);
  }, [toutPose, fini, etat, a, onFin]);

  const former = (g: string, d: string) => {
    if (fini || etat.poses[g] || gPour(d) !== undefined || faute) return;
    setChoisi(null);
    const r = retourDe(a, g, d);
    if (r.juste) {
      setEtat(e => ({ ...e, poses: { ...e.poses, [g]: d } }));
      setDernier(r);
      voix.current = Promise.resolve(onPaire(r, g, d));
      return;
    }
    const n = (etat.erreurs[g] || 0) + 1;
    setEtat(e => ({ ...e, erreurs: { ...e.erreurs, [g]: n } }));
    setFaute({ g, d });
    setDernier(r);
    voix.current = Promise.resolve(onPaire(r, g, d));
    window.setTimeout(() => {
      setFaute(null);
      if (n < essais) return;
      // trop d'erreurs sur cet élément : la bonne paire est posée pour lui, avec son retour
      const bonne = a.couples[g];
      if (!bonne) return;
      const rb = retourDe(a, g, bonne);
      setEtat(e => (e.poses[g] ? e : { ...e, poses: { ...e.poses, [g]: bonne }, donnees: [...e.donnees, g] }));
      setDernier({ ...rb, donnee: true });
      voix.current = voix.current.then(() => onPaire({ ...rb, juste: true }, g, bonne, true));
    }, FAUTE_MS);
  };

  const toucher = (cote: 'g' | 'd', id: string) => {
    if (fini || faute) return;
    if (cote === 'g' ? etat.poses[id] : gPour(id) !== undefined) return;
    if (!choisi || choisi.cote === cote) { setChoisi(choisi?.cote === cote && choisi.id === id ? null : { cote, id }); return; }
    if (cote === 'd') former(choisi.id, id); else former(id, choisi.id);
  };

  // Glisser (souris et doigt) : la prise suit le pointeur ; lâchée sur un élément de l'autre colonne, la paire est formée.
  // Un appui sans mouvement est un toucher.
  const appui = (cote: 'g' | 'd', id: string) => (ev: ReactPointerEvent) => {
    if (fini || faute || ev.button > 0) return;
    if (cote === 'g' ? etat.poses[id] : gPour(id) !== undefined) return;
    const p = { cote, id, x: ev.clientX, y: ev.clientY, glisse: false };
    priseRef.current = p; setPrise(p);
  };
  useEffect(() => {
    if (!prise) return;
    const bouge = (ev: PointerEvent) => {
      const p = priseRef.current;
      if (!p) return;
      const glisse = p.glisse || Math.hypot(ev.clientX - p.x, ev.clientY - p.y) > 8;
      const n = { ...p, x: ev.clientX, y: ev.clientY, glisse };
      priseRef.current = n; setPrise(n);
    };
    const lache = (ev: PointerEvent) => {
      const p = priseRef.current;
      priseRef.current = null; setPrise(null);
      if (!p) return;
      if (!p.glisse) { toucher(p.cote, p.id); return; }
      const cible = (document.elementFromPoint(ev.clientX, ev.clientY) as HTMLElement | null)?.closest('[data-assoc]') as HTMLElement | null;
      const [cote, id] = (cible?.dataset.assoc || '').split(':');
      if (!cote || !id || cote === p.cote) return;
      if (p.cote === 'g') former(p.id, id); else former(id, p.id);
    };
    const annule = () => { priseRef.current = null; setPrise(null); };
    window.addEventListener('pointermove', bouge);
    window.addEventListener('pointerup', lache);
    window.addEventListener('pointercancel', annule);
    return () => { window.removeEventListener('pointermove', bouge); window.removeEventListener('pointerup', lache); window.removeEventListener('pointercancel', annule); };
  // eslint-disable-next-line react-hooks/exhaustive-deps -- les gestionnaires lisent l'état du moment par la prise
  }, [prise !== null, etat, choisi, faute, fini]);

  // Écran bas (portable 1366×560, téléphone en paysage) : tout tient sans défiler (règle « tableaux sans défilement »).
  const bas = useEcran('(max-height: 700px)');
  const telephone = useEcran('(max-height: 520px) and (orientation: landscape)');
  const serre = compact || bas;
  const texte = serre ? 'text-[15px]' : 'text-base';   // jamais sous 15 px (skill logique-de-cours, règle 9)
  const aCommence = Object.keys(etat.poses).length > 0 || Object.values(etat.erreurs).some(Boolean);
  const libelle = (id: string, t: string) => (
    <><span className="mr-1 font-bold text-amber-100">{id}-</span><Formule t={t} /></>
  );
  const element = (cote: 'g' | 'd', id: string, t: string) => {
    const g = cote === 'g' ? id : gPour(id);
    const pose = g !== undefined && (cote === 'g' ? !!etat.poses[id] : true);
    const enFaute = faute && (cote === 'g' ? faute.g === id : faute.d === id);
    const sel = (choisi?.cote === cote && choisi.id === id) || (prise?.glisse && prise.cote === cote && prise.id === id);
    const donnee = pose && g !== undefined && etat.donnees.includes(g);
    const partenaire = cote === 'g' ? etat.poses[id] : g;
    return (
      <button key={id} type="button" data-assoc={`${cote}:${id}`} onPointerDown={appui(cote, id)}
        onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toucher(cote, id); } }}
        disabled={fini && !pose} aria-pressed={!!sel}
        className={`relative flex w-full select-none items-start gap-1 rounded-lg border px-2.5 ${telephone ? 'py-0.5' : serre ? 'py-1' : 'py-1.5'} text-left leading-snug transition-colors ${texte} ${
          enFaute ? 'border-rose-400 bg-rose-500/25' : pose ? (donnee ? 'border-amber-300/70 bg-amber-400/10' : 'border-emerald-400/80 bg-emerald-500/15')
            : sel ? 'border-cyan-300 bg-cyan-400/20' : 'border-white/20 hover:bg-white/10'}`}
        style={{ touchAction: 'none', fontFamily: 'system-ui, sans-serif', boxShadow: pose && g !== undefined ? `inset ${cote === 'g' ? '' : '-'}6px 0 0 ${couleurDe(g)}` : undefined }}>
        <span className="min-w-0 flex-1">{libelle(id, t)}</span>
        {pose && partenaire && (
          <span className="shrink-0 rounded-full px-1.5 text-[15px] font-bold leading-snug text-black" style={{ background: couleurDe(g!) }}>
            {cote === 'g' ? `→ ${partenaire}` : `← ${partenaire}`}
          </span>
        )}
      </button>
    );
  };

  // Le retour de la dernière paire : sous les colonnes ; au-dessus sur téléphone en paysage, pour être lu sans défiler.
  const retourEcrit = dernier && (
    <p role="status" className={`${telephone ? 'mt-0.5 text-[15px] leading-snug' : serre ? 'mt-1 text-base' : 'mt-2 text-lg'} ${dernier.juste ? 'text-emerald-200' : 'text-rose-200'}`}>
      {dernier.donnee ? '➜ La bonne paire : ' : dernier.juste ? '✔ ' : '↻ '}<Formule t={dernier.texte} />
    </p>
  );

  return (
    <div data-association className={telephone ? 'mt-1' : 'mt-2'}>
      {dernier && !fini && telephone && retourEcrit}
      {!fini && !toutPose && !aCommence && !telephone && (
        <p className="text-[15px] text-white/55" style={{ fontFamily: 'system-ui, sans-serif' }}>
          Glisse un élément sur son partenaire, ou touche l’un puis l’autre.
        </p>
      )}
      {telephone ? (
        // Téléphone en paysage : la colonne de gauche en une rangée au-dessus, la droite sur toute la largeur.
        <div className="mt-0.5 flex flex-col gap-[3px]">
          <div className="grid gap-[3px]" style={{ gridTemplateColumns: `repeat(${a.gauche.length <= 3 ? a.gauche.length : 2}, minmax(0, 1fr))` }}>
            {a.gauche.map(x => element('g', x.id, x.texte))}
          </div>
          {droite.map(x => element('d', x.id, x.texte))}
        </div>
      ) : (
        <div className={`${serre ? 'mt-1' : 'mt-2'} grid gap-2`} style={{ gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 2.3fr)' }}>
          <div className={`flex flex-col ${serre ? 'gap-1' : 'gap-1.5'}`}>{a.gauche.map(x => element('g', x.id, x.texte))}</div>
          <div className={`flex flex-col ${serre ? 'gap-1' : 'gap-1.5'}`}>{droite.map(x => element('d', x.id, x.texte))}</div>
        </div>
      )}
      {dernier && !fini && !telephone && retourEcrit}
      {prise?.glisse && actif && createPortal(
        <div className="pointer-events-none fixed z-[100] -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-200 bg-cyan-500/80 px-3 py-1 text-sm font-bold text-white shadow-lg"
          style={{ left: prise.x, top: prise.y, fontFamily: 'system-ui, sans-serif' }}>
          {prise.id}
        </div>,
        document.body,
      )}
    </div>
  );
}
