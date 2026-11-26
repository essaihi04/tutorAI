import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Pause, Play, SkipForward, Volume2 } from 'lucide-react';
import '../session/AIAvatar.css';
import type { ProfessorMood } from '../session/Professor3D';
import type { ProfessorGestureKind } from '../../services/professorEmotion';

const Professor3D = lazy(() => import('../session/Professor3D'));

/**
 * Le tableau vivant de la landing (26 novembre 2026).
 *
 * Pas de vidéo enregistrée : ce sont de VRAIES diapositives des cours (scripts/extraits_landing.py les relève dans
 * les fichiers de cours), rejouées comme dans le lecteur : l'animation « au tableau » dans son cadre, la piste de voix
 * publiée, et les commandes du tuteur envoyées à l'animation au mot où la voix les dit (`play_until`…). Le VRAI tuteur
 * 3D de la séance salue, parle et montre le tableau. Une vidéo vieillit dès qu'un cours change ; ici la vitrine montre
 * toujours le cours d'aujourd'hui, nette à toute taille d'écran.
 *
 * Sans le son (les navigateurs interdisent de le lancer sans un geste), la même diapositive se joue sur une horloge,
 * avec les sous-titres français dans la bulle du tuteur. Un bouton donne la voix : la diapositive repart avec elle.
 *
 * Chaque animation est dessinée pour un cadre de 1120 × 630 px puis mise à l'échelle du cadre réel : le dessin est le
 * même sur un téléphone et sur un grand écran (les pages adaptent sinon leur disposition à la largeur).
 */

export interface Extrait {
  id: string;
  onglet: string;
  matiere: string;
  /** Ce que l'extrait montre du tuteur (« Il corrige le national »…). */
  capacite: string;
  cours: string;
  titre: string;
  src: string;
  /** Sans piste (la feuille du sujet, montrée avant sa correction) : la diapositive se joue sur l'horloge. */
  audio: string | null;
  duree: number;
  /** Un examen : son titre et son année, écrits en haut du tableau, dès la feuille du sujet. */
  entete?: { titre: string; sujet: string };
  demarrer: string | null;
  commandes: { t: number; commande: string; parametres: Record<string, unknown> }[];
  /** Les instants où le tuteur montre quelque chose au tableau. */
  pointes: number[];
  sous_titres: { t: number; texte: string }[];
}

const L = 1120, H = 630;

/**
 * Une animation de cours dans son cadre, à l'échelle. `actif` : montée seulement quand elle est à l'écran.
 * Sans `onCadre`, la page joue seule (on lui envoie `start`, comme le lecteur) ; avec, c'est l'appelant qui la pilote.
 */
export function CadreAnimation({ src, titre, actif = true, cle = 0, onCadre }: {
  src: string; titre: string; actif?: boolean; cle?: number; onCadre?: (cadre: HTMLIFrameElement) => void;
}) {
  const boite = useRef<HTMLDivElement>(null);
  const [k, setK] = useState(0);
  useEffect(() => {
    const el = boite.current;
    if (!el) return;
    const mesurer = () => setK(el.clientWidth / L);
    mesurer();
    const obs = new ResizeObserver(mesurer);
    obs.observe(el);
    return () => obs.disconnect();
  }, []);
  const charge = (cadre: HTMLIFrameElement) => {
    if (onCadre) { onCadre(cadre); return; }
    setTimeout(() => cadre.contentWindow?.postMessage({ type: 'simulation_control', command: 'start', parameters: {} }, '*'), 500);
  };
  return (
    <div ref={boite} className="relative w-full overflow-hidden" style={{ aspectRatio: `${L} / ${H}` }}>
      {actif && k > 0 && (
        <iframe
          key={`${src}#${cle}`}
          src={src}
          title={titre}
          tabIndex={-1}
          onLoad={e => charge(e.currentTarget)}
          className="absolute left-0 top-0 border-0 pointer-events-none"
          style={{ width: L, height: H, transform: `scale(${k})`, transformOrigin: '0 0' }}
        />
      )}
    </div>
  );
}

/** Vrai quand l'élément est (en partie) à l'écran : rien ne tourne hors de vue. */
export function useVisible<T extends HTMLElement>(seuil = 0.25) {
  const ref = useRef<T>(null);
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === 'undefined') { setVisible(true); return; }
    const obs = new IntersectionObserver(([e]) => setVisible(e.isIntersecting), { threshold: seuil });
    obs.observe(el);
    return () => obs.disconnect();
  }, [seuil]);
  return [ref, visible] as const;
}

/**
 * Le mot de bienvenue du tuteur, avant le premier extrait : il présente la plateforme et met en confiance
 * (26 novembre 2026 : pas ChatGPT, un prof spécialisé dans le bac marocain, en darija, les cours et chaque question des
 * nationaux pas à pas, le mode libre, « je te comprends et je connais ton niveau », « toi et moi, le bac avec mention »).
 * Avec le son, la voix (media/audio/landing/bienvenue.mp3, voix Bodi) mène et les bulles la suivent (`poids` : part de
 * la piste) ; sans le son, chaque bulle reste le temps de la lire (`duree`).
 */
const BIENVENUE = [
  { poids: .17, duree: 4, texte: <><span className="font-brand" dir="rtl">مرحبا بيك</span> 👋 Moi, c'est Moalim. Pas ChatGPT : un prof spécialisé dans le bac marocain.</> },
  { poids: .33, duree: 5, texte: <>Je t'explique en darija, pas à pas, comme un vrai prof : tous les cours, et chaque question des examens nationaux.</> },
  { poids: .14, duree: 3.6, texte: <>En mode libre, pose-moi n'importe quelle question : je te réponds.</> },
  { poids: .17, duree: 3.6, texte: <>Je te comprends, je connais ton niveau, et on progresse ensemble.</> },
  { poids: .19, duree: 4.2, texte: <>Je suis avec toi à la maison, à toute heure. Toi et moi, on va décrocher le bac avec mention !</> },
];
const VOIX_BIENVENUE = '/media/audio/landing/bienvenue.mp3';
/** Silence laissé après la voix avant la diapositive suivante (s). */
const RESPIRATION = 1.6;
/** Le tuteur garde le bras tendu ce temps-là après chaque pointage (s). */
const TENUE_POINTAGE = 2.4;

export default function TableauVivant({ extraits, couleurs }: { extraits: Extrait[]; couleurs: Record<string, string> }) {
  const [i, setI] = useState(0);
  const [tour, setTour] = useState(0);
  const [pause, setPause] = useState(false);
  const [son, setSon] = useState(false);
  /** L'animation a déclaré son protocole : la diapositive peut partir. */
  const [pret, setPret] = useState(false);
  /** Le temps de la diapositive (s), rafraîchi quatre fois par seconde pour la bulle et la gouttière. */
  const [t, setT] = useState(0);
  /** La bulle de bienvenue en cours (−1 : la bienvenue est dite). */
  const [accueil, setAccueil] = useState(0);
  const [zone, visible] = useVisible<HTMLDivElement>(0.3);
  const tableau = useRef<HTMLDivElement>(null);
  const cadre = useRef<HTMLIFrameElement | null>(null);
  const voix = useRef<HTMLAudioElement>(null);
  const e = extraits[i];
  /** Les onglets : une matière, ses extraits consécutifs dans la liste. */
  const onglets = useMemo(() => extraits.reduce<{ nom: string; debut: number; nombre: number }[]>((acc, d, n) => {
    const der = acc[acc.length - 1];
    if (der && der.nom === d.onglet) der.nombre++;
    else acc.push({ nom: d.onglet, debut: n, nombre: 1 });
    return acc;
  }, []), [extraits]);
  const couleur = couleurs[e.matiere] || '#facc15';
  const bienvenue = accueil >= 0;
  const joue = visible && !pause && pret && !bienvenue;

  const envoyer = useCallback((commande: string, parametres: Record<string, unknown> = {}) => {
    cadre.current?.contentWindow?.postMessage({ type: 'simulation_control', command: commande, parameters: parametres }, '*');
  }, []);

  // ── Une nouvelle diapositive : on attend que l'animation se déclare, puis on lui donne son départ ──
  const horloge = useRef(0), envoyees = useRef(0);
  useEffect(() => { setPret(false); setT(0); horloge.current = 0; envoyees.current = 0; cadre.current = null; }, [i, tour]);
  const onCadre = useCallback((el: HTMLIFrameElement) => { cadre.current = el; }, []);
  useEffect(() => {
    if (pret) return;
    const partir = () => { if (e.demarrer) envoyer(e.demarrer); setPret(true); };
    const ecoute = (m: MessageEvent) => {
      // Le manifeste part souvent avant l'événement « load » : on reconnaît le cadre par sa fenêtre.
      const el = tableau.current?.querySelector('iframe');
      if (el && m.source === el.contentWindow && m.data?.type === 'simulation_manifest') { cadre.current = el; partir(); }
    };
    window.addEventListener('message', ecoute);
    const secours = setInterval(() => { if (cadre.current) partir(); }, 2500);   // page sans manifeste : on part quand même
    return () => { window.removeEventListener('message', ecoute); clearInterval(secours); };
  }, [pret, e, envoyer, i, tour]);

  // ── La bienvenue : coucou et bulles, une seule fois ──
  const [gesture, setGesture] = useState<{ kind: ProfessorGestureKind; key: number } | null>(null);
  useEffect(() => {
    if (!visible || accueil < 0) return;
    const a = accueil === 0 ? setTimeout(() => setGesture({ kind: 'wave', key: Date.now() }), 250) : undefined;
    // avec le son, c'est la voix qui fait avancer les bulles (plus bas)
    const b = son ? undefined : setTimeout(() => setAccueil(n => (n + 1 < BIENVENUE.length ? n + 1 : -1)), BIENVENUE[accueil].duree * 1000);
    return () => { clearTimeout(a); clearTimeout(b); };
  }, [visible, accueil, son]);
  // L'élève a déjà fait un geste sur la page (la visite guidée du survol…) : le tableau parle tout de suite.
  const vuUneFois = useRef(false);
  useEffect(() => {
    if (!visible || vuUneFois.current) return;
    vuUneFois.current = true;
    if ((navigator as Navigator & { userActivation?: { hasBeenActive: boolean } }).userActivation?.hasBeenActive) setSon(true);
  }, [visible]);
  // La voix de la bienvenue : elle mène les bulles, puis laisse la place au premier extrait.
  const voixAccueil = useRef<HTMLAudioElement>(null);
  const enAccueil = accueil >= 0;
  useEffect(() => {
    const a = voixAccueil.current;
    if (!a) return;
    if (visible && son && enAccueil && !pause) a.play().catch((err: DOMException) => { if (err?.name === 'NotAllowedError') setSon(false); });
    else a.pause();
  }, [visible, son, enAccueil, pause]);
  const suivreAccueil = () => {
    const a = voixAccueil.current;
    if (!a || !isFinite(a.duration) || accueil < 0) return;
    let u = a.currentTime / a.duration, k = 0;
    while (k < BIENVENUE.length - 1 && u > BIENVENUE[k].poids) { u -= BIENVENUE[k].poids; k++; }
    if (k !== accueil) setAccueil(k);
  };

  // ── La voix : elle suit lecture et pause ; sans le son, une horloge la remplace ──
  useEffect(() => {
    const a = voix.current;
    if (!a) return;
    // Lecture refusée par le navigateur (pas de geste) : on continue en muet. Une lecture seulement interrompue par
    // une pause (AbortError, au changement de diapositive) n'est pas un refus.
    if (son && joue && e.audio) a.play().catch((err: DOMException) => { if (err?.name === 'NotAllowedError') setSon(false); });
    else a.pause();
  }, [son, joue, i, tour, e.audio]);

  const suivant = useCallback(() => { setI(n => (n + 1) % extraits.length); setTour(n => n + 1); }, [extraits.length]);
  useEffect(() => {
    if (!joue) return;
    const PAS = 0.1;
    let dernier = -1;
    const battre = setInterval(() => {
      const a = voix.current;
      const maintenant = son && a && e.audio ? (a.ended ? e.duree + (horloge.current += PAS) : a.currentTime) : (horloge.current += PAS);
      while (envoyees.current < e.commandes.length && e.commandes[envoyees.current].t <= maintenant) {
        const c = e.commandes[envoyees.current++];
        envoyer(c.commande, c.parametres);
      }
      if (Math.floor(maintenant * 4) !== dernier) { dernier = Math.floor(maintenant * 4); setT(maintenant); }
      if (maintenant >= e.duree + RESPIRATION) { setGesture({ kind: 'cheer', key: Date.now() }); suivant(); }
    }, PAS * 1000);
    return () => clearInterval(battre);
  }, [joue, son, e, envoyer, suivant]);

  /** Le geste de l'élève (un clic) autorise la piste : sans lui, le navigateur refuse de lancer le son. */
  const autoriserSon = () => { const a = voix.current; if (a) { a.play().catch(() => {}); a.pause(); a.currentTime = 0; } };
  /** Choisir une matière : son extrait part du début, avec la voix (le clic sur l'onglet vaut geste). */
  const choisir = (n: number) => { autoriserSon(); setSon(true); setI(n); setTour(k => k + 1); setPause(false); setAccueil(-1); };
  /** Donner la voix : le geste de l'élève autorise le son ; la diapositive repart du début avec elle. */
  const basculerSon = () => {
    const a = voix.current;
    if (!son && a) autoriserSon();
    // Donner la voix pendant la bienvenue : elle repart du début, dite cette fois ; couper la voix la saute.
    const garder = !son && accueil >= 0;
    if (garder && voixAccueil.current) { voixAccueil.current.currentTime = 0; setAccueil(0); } else setAccueil(-1);
    setSon(s => !s); setPause(false); setTour(k => k + 1);
  };

  // ── Le tuteur : il parle pendant la voix et montre le tableau aux instants de pointage ──
  const parle = joue && t < e.duree;
  const pointe = parle && e.pointes.concat(e.commandes.map(c => c.t)).some(p => t >= p && t < p + TENUE_POINTAGE);
  const [cible, setCible] = useState<{ x: number; y: number } | null>(null);
  useEffect(() => {
    if (!pointe) { setCible(null); return; }
    const r = tableau.current?.getBoundingClientRect();
    if (r) setCible({ x: r.left + r.width * 0.5, y: r.top + r.height * 0.5 });
  }, [pointe]);
  const mood: ProfessorMood = bienvenue || parle ? 'speaking' : 'idle';
  const [sans3D, setSans3D] = useState(false);
  const rien = useCallback(() => {}, []);
  const echec3D = useCallback(() => setSans3D(true), []);

  const phrase = [...e.sous_titres].reverse().find(s => s.t <= t)?.texte ?? e.sous_titres[0]?.texte ?? '';
  const avance = Math.min(1, t / e.duree);
  /** La feuille d'un examen s'ouvre sur son titre seul, le temps de le lire (s). */
  const titreSeul = !!e.entete && !e.audio && t < 2.4;

  return (
    <div ref={zone} className="lp-scene relative">
      <div className="lp-plateau">
      <audio ref={voix} src={e.audio ?? undefined} preload={son ? 'auto' : 'none'} />
      <audio ref={voixAccueil} src={VOIX_BIENVENUE} preload="auto" onTimeUpdate={suivreAccueil} onEnded={() => setAccueil(-1)} onError={() => setAccueil(-1)} />

      {/* Les matières : des étiquettes à la craie ; chacune a ses extraits, joués l'un après l'autre (un point par extrait) */}
      <div className="flex items-end gap-1 sm:gap-1.5 pl-2 sm:pl-5" role="tablist" aria-label="Matière">
        {onglets.map(o => {
          const actif = o.nom === e.onglet;
          const c = couleurs[extraits[o.debut].matiere];
          return (
            <button key={o.nom} role="tab" aria-selected={actif} onClick={() => choisir(o.debut)}
              className="craie relative px-2.5 sm:px-3.5 pt-1.5 pb-1 rounded-t-xl text-[15px] sm:text-lg leading-none transition-all"
              style={actif
                ? { background: '#5b4028', color: c, boxShadow: `inset 0 2px 0 ${c}` }
                : { background: 'rgba(91,64,40,.45)', color: 'rgba(226,232,240,.6)' }}>
              {o.nom}
              {actif && o.nombre > 1 && (
                <span className="flex justify-center gap-1 mt-0.5" aria-hidden>
                  {Array.from({ length: o.nombre }, (_, k) => (
                    <span key={k} className="w-1 h-1 rounded-full" style={{ background: o.debut + k === i ? c : 'rgba(226,232,240,.35)' }} />
                  ))}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Le tableau : cadre en bois, ardoise verte, gouttière à craies */}
      <div className="relative rounded-2xl p-2 sm:p-2.5 shadow-[0_30px_80px_-20px_rgba(0,0,0,.8)]"
        style={{ background: 'linear-gradient(160deg,#7a5836 0%,#5b4028 45%,#3f2c1b 100%)' }}>
        <div ref={tableau} className="relative rounded-lg overflow-hidden"
          style={{ background: 'radial-gradient(ellipse at 50% 35%,#13241e 0,#0f1d18 55%,#0a1410 100%)', boxShadow: 'inset 0 0 40px rgba(0,0,0,.55)' }}>
          <CadreAnimation src={e.src} titre={`${e.cours} — ${e.titre}`} actif={visible} cle={tour} onCadre={onCadre} />

          {/* Bandeau : ce que l'on regarde */}
          <div className="absolute left-0 right-0 bottom-0 flex items-center gap-2 px-3 pt-4 pb-1.5 text-[11px] sm:text-xs bg-gradient-to-t from-black/75 to-transparent pointer-events-none">
            <span className="craie shrink-0 px-2 py-0.5 rounded-full text-sm leading-none text-black" style={{ background: couleur }}>{e.capacite}</span>
            <span className="font-semibold text-white/90 truncate">
              {e.cours} <span className="text-white/55 font-normal hidden sm:inline">· {e.titre}</span>
            </span>
          </div>

          {/* Un examen : d'abord son titre et son année, seuls sur le tableau, puis en bandeau au-dessus de la feuille */}
          {e.entete && (titreSeul ? (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-1 sm:gap-2 bg-[#0f1d18]/95 text-center px-4 pb-[16%] pointer-events-none">
              <div className="craie text-xl sm:text-2xl xl:text-4xl leading-none" style={{ color: couleur }}>{e.entete.titre}</div>
              <div className="craie text-[15px] sm:text-lg xl:text-2xl leading-tight text-white/85">{e.entete.sujet}</div>
            </div>
          ) : (
            <div className="absolute left-2 top-2 max-w-[calc(100%-6.5rem)] px-2.5 py-1 rounded-lg bg-[#0f1d18]/90 shadow-lg pointer-events-none">
              <div className="craie text-sm sm:text-lg leading-none truncate" style={{ color: couleur }}>{e.entete.titre}</div>
              <div className="text-[10px] sm:text-xs leading-tight text-white/75 truncate">{e.entete.sujet}</div>
            </div>
          ))}

          {/* Les commandes */}
          <div className="absolute right-2 top-2 flex items-center gap-1.5">
            <button onClick={() => setPause(p => !p)} aria-label={pause ? 'Reprendre' : 'Mettre en pause'}
              className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-black/55 text-white/85 hover:bg-black/80 transition-colors">
              {pause ? <Play className="w-4 h-4" /> : <Pause className="w-4 h-4" />}
            </button>
            <button onClick={() => { setAccueil(-1); suivant(); }} aria-label="Extrait suivant"
              className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-black/55 text-white/85 hover:bg-black/80 transition-colors">
              <SkipForward className="w-4 h-4" />
            </button>
            {son && (
              <button onClick={basculerSon} aria-label="Couper la voix"
                className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-yellow-300 text-black hover:bg-yellow-200 transition-colors">
                <Volume2 className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Sans le son : l'invitation à écouter, au milieu du bas du tableau */}
          {!son && (
            <button onClick={basculerSon}
              className="lp-ecoute absolute left-1/2 -translate-x-1/2 bottom-9 sm:bottom-11 inline-flex items-center gap-2 pl-3 pr-4 py-2 rounded-full bg-yellow-300 text-black font-bold text-sm whitespace-nowrap shadow-xl hover:bg-yellow-200 transition-colors">
              <Play className="w-4 h-4 fill-current" /> Écouter Moalim expliquer
            </button>
          )}
        </div>

        {/* La gouttière : la diapositive s'y écoule, deux craies posées */}
        <div className="relative mt-2 h-2.5 rounded-sm bg-black/35 overflow-hidden">
          <div className="h-full rounded-sm transition-[width] duration-300 ease-linear" style={{ background: couleur, width: `${avance * 100}%` }} />
        </div>
        <span className="absolute bottom-[3px] right-10 h-2 w-9 rounded-sm bg-slate-100 rotate-[-3deg] shadow" />
        <span className="absolute bottom-[3px] right-24 h-2 w-6 rounded-sm bg-yellow-300 rotate-[4deg] shadow" />
      </div>

      </div>

      {/* Le tuteur, debout sous le tableau : sa bulle porte ce qu'il dit (en français, la voix est en darija) */}
      <div className="lp-tuteur absolute pointer-events-none">
        <div className={`lp-bulle craie ${bienvenue || parle ? 'lp-bulle--dite' : ''}`}>
          {bienvenue ? BIENVENUE[accueil].texte : phrase}
        </div>
        {sans3D
          ? <img src="/media/avatar/moalim-professeur.png" alt="Moalim, ton professeur virtuel" className="block w-[180px] h-[260px] object-contain" draggable={false} />
          : <Suspense fallback={<img src="/media/avatar/moalim-professeur.png" alt="Moalim, ton professeur virtuel" className="block w-[180px] h-[260px] object-contain" />}>
              <Professor3D mood={mood} pointing={!!cible} pointingSide="right" target={cible} onHandPosition={rien} gesture={gesture} onError={echec3D} />
            </Suspense>}
      </div>
    </div>
  );
}
