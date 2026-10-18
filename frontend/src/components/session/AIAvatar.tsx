import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState, type CSSProperties } from 'react';
import { createPortal } from 'react-dom';
import type { ScientificControlCommand } from './scientific/types';
import './AIAvatar.css';
import { PROFESSOR_FOCUS, PROFESSOR_REACH_MS } from '../../services/professorFocus';
import { PROFESSOR_EMOTIONS, type ProfessorEmotionKind, type ProfessorGestureKind } from '../../services/professorEmotion';
import type { ProfessorMotion, ProfessorRig } from './Professor3D';
const Professor3D = lazy(() => import('./Professor3D'));

/** Commande du tuteur pour un laboratoire HTML (iframe) : le professeur appuie, puis le message part. */
export interface LabControlCommand {
  sequence: number;
  command: string;
  /** Message `simulation_control` à transmettre à l'iframe une fois le bouton appuyé. */
  message: Record<string, unknown>;
}

interface AIAvatarProps {
  isSpeaking: boolean;
  isProcessing: boolean;
  processingStage?: string;
  control?: ScientificControlCommand | null;
  labControl?: LabControlCommand | null;
  /** Émotion à exprimer (salut, bravo, affection…) : geste du personnage et émoticônes qui s'envolent de lui. */
  emotion?: { kind: ProfessorEmotionKind; key: number } | null;
}
type Spark = { id: number; emoji: string; x: number; y: number; dx: number; delay: number; size: number };
const WIDTH = 180;
const HEIGHT = 320;
/** Mesures par défaut, remplacées par celles du modèle dès qu'il est chargé (onRig). */
const DEFAULT_RIG: ProfessorRig = { shoulderRight: { x: 61, y: 105 }, shoulderLeft: { x: 119, y: 105 }, reach: 112 };
const clampPosition = (x: number, y: number) => ({
  x: Math.max(-40, Math.min(x, window.innerWidth - WIDTH + 40)),
  y: Math.max(0, Math.min(y, window.innerHeight - HEIGHT)),
});
/** En vol vers une cible, il peut descendre plus bas : ses jambes peuvent sortir de l'écran. */
const clampFlight = (x: number, y: number) => ({
  x: Math.max(-60, Math.min(x, window.innerWidth - WIDTH + 60)),
  y: Math.max(-20, Math.min(y, window.innerHeight - 150)),
});
/** Délai sans cible avant qu'il ne retourne à sa place. */
const RETURN_HOME_MS = 1600;
type Point = { x: number; y: number };
type Focus = { rect: DOMRect; writing: boolean };

/**
 * Place la boîte pour que la main du professeur atteigne `point`. Avec `avoid` (le panneau de simulation
 * ou la scène montrée), il se tient à côté du panneau, jamais dessus : la baguette fait la liaison.
 */
function reachPosition(point: Point, writing: boolean, rig: ProfessorRig, avoid?: DOMRect | null) {
  const { shoulderRight: right, shoulderLeft: left, reach } = rig;
  if (avoid && !writing) {
    const y = point.y - right.y + reach * 0.16;
    if (avoid.right + 12 + WIDTH <= window.innerWidth) return clampFlight(avoid.right + 12, y);      // à droite du panneau
    if (avoid.left - 12 - WIDTH >= 0) return clampFlight(avoid.left - 12 - WIDTH, y);               // à gauche
  }
  if (writing) {
    // Écriture : il flotte juste sous la ligne, tête comprise (le haut du personnage est à ~16 px du
    // haut de la boîte), sa main droite levée vers le trait ; une baguette relie la main à la plume.
    return clampFlight(point.x - right.x + reach * 0.75, point.y + 4);
  }
  // Pointage : bras droit si la place existe à droite de la cible, sinon bras gauche depuis la gauche.
  const fromRight = point.x + reach - right.x + WIDTH < window.innerWidth + 40;
  return fromRight
    ? clampFlight(point.x + reach * 0.92 - right.x, point.y - right.y + reach * 0.16)
    : clampFlight(point.x - reach * 0.92 - left.x, point.y - left.y + reach * 0.16);
}

export default function AIAvatar({ isSpeaking, isProcessing, processingStage, control, labControl, emotion }: AIAvatarProps) {
  const initial = useMemo(() => clampPosition(window.innerWidth - WIDTH - 20, window.innerHeight - HEIGHT - 100), []);
  const [minimized, setMinimized] = useState(false);
  const [animationFailed, setAnimationFailed] = useState(false);
  const onAnimationError = useCallback(() => setAnimationFailed(true), []);
  const [focus, setFocus] = useState<Focus | null>(null);
  const [press, setPress] = useState<{ key: number; x: number; y: number } | null>(null);
  const deliveredLab = useRef(0);
  const [gesture, setGesture] = useState<{ kind: ProfessorGestureKind; key: number } | null>(null);
  const [sparks, setSparks] = useState<Spark[]>([]);
  const sparkId = useRef(0);
  const [hand, setHand] = useState<Point | null>(null);
  const onHandPosition = useCallback((next: Point) => setHand(previous =>
    previous && Math.abs(previous.x - next.x) + Math.abs(previous.y - next.y) < 1 ? previous : next), []);
  const [portalRoot, setPortalRoot] = useState<Element>(document.fullscreenElement || document.body);
  const box = useRef<HTMLDivElement>(null);
  const goal = useRef<Point>(initial);            // là où il vole
  const home = useRef<Point>(initial);            // sa place de repos, choisie par l'élève
  const current = useRef<Point>({ ...initial });  // là où il est
  const motion = useRef<ProfessorMotion>({ vx: 0, vy: 0 });
  const rig = useRef<ProfessorRig>(DEFAULT_RIG);
  const onRig = useCallback((measured: ProfessorRig) => { rig.current = measured; }, []);
  const [side, setSide] = useState<'left' | 'right'>('left');
  const drag = useRef<{ x: number; y: number; left: number; top: number } | null>(null);
  const state = isSpeaking ? 'speaking' : isProcessing ? 'thinking' : 'idle';
  const status = isSpeaking ? 'Je parle…' : isProcessing
    ? processingStage === 'stt' ? 'Je t’écoute…' : processingStage === 'tts' ? 'Préparation audio…' : 'Je réfléchis…'
    : 'Prêt à t’aider';

  const fly = useCallback((next: Point, immediate = false) => {
    goal.current = next;
    if (immediate) { current.current = { ...next }; motion.current.vx = 0; motion.current.vy = 0; }
  }, []);
  const aimSide = useCallback((point: Point) => setSide(point.x > goal.current.x + WIDTH / 2 ? 'right' : 'left'), []);

  // Émotion : le geste part, et les émoticônes jaillissent de sa tête, là où il se trouve à cet instant.
  const express = useCallback((kind: ProfessorEmotionKind, key: number) => {
    const spec = PROFESSOR_EMOTIONS[kind];
    if (spec.gesture) setGesture({ kind: spec.gesture, key });
    const origin = { x: current.current.x + WIDTH / 2, y: current.current.y + 52 };
    const batch: Spark[] = Array.from({ length: spec.count }, (_, i) => ({
      id: ++sparkId.current, emoji: spec.emojis[i % spec.emojis.length],
      x: origin.x + (Math.random() - 0.5) * 70, y: origin.y + (Math.random() - 0.5) * 30,
      dx: (Math.random() - 0.5) * 90, delay: i * 0.12, size: 18 + Math.random() * 14,
    }));
    setSparks(previous => [...previous, ...batch].slice(-40));                       // jamais plus de 40 à la fois
    window.setTimeout(() => setSparks(previous => previous.filter(spark => !batch.includes(spark))), 3400);
  }, []);
  useEffect(() => {
    if (!emotion) return;
    const timer = window.setTimeout(() => express(emotion.kind, emotion.key), 0);
    return () => window.clearTimeout(timer);
  }, [emotion, express]);

  // Vol : ressort amorti vers la cible, élévation et inclinaison dans le sens du vol, flottement à l'arrêt.
  useEffect(() => {
    let frame = 0, last = performance.now();
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    const step = (now: number) => {
      const dt = Math.min(0.05, (now - last) / 1000); last = now;
      const element = box.current, p = current.current, g = goal.current, m = motion.current;
      if (reduced.matches) { p.x = g.x; p.y = g.y; m.vx = 0; m.vy = 0; }
      else {
        const k = 38, c = 2 * Math.sqrt(k);
        m.vx += ((g.x - p.x) * k - m.vx * c) * dt;
        m.vy += ((g.y - p.y) * k - m.vy * c) * dt;
        p.x += m.vx * dt; p.y += m.vy * dt;
      }
      if (element) {
        const speed = Math.hypot(m.vx, m.vy);
        const lift = Math.min(26, speed * 0.04);
        const hover = reduced.matches ? 0 : Math.sin(now / 600) * 3;
        const tilt = Math.max(-12, Math.min(12, m.vx * 0.012));
        element.style.transform = `translate(${p.x}px, ${p.y - lift + hover}px) rotate(${tilt}deg)`;
        element.dataset.flying = speed > 60 ? 'true' : 'false';
      }
      frame = requestAnimationFrame(step);
    };
    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame);
  }, []);

  useEffect(() => {
    const resize = () => { home.current = clampPosition(home.current.x, home.current.y); fly(clampFlight(goal.current.x, goal.current.y)); };
    window.addEventListener('resize', resize);
    return () => window.removeEventListener('resize', resize);
  }, [fly]);

  useEffect(() => {
    const update = () => setPortalRoot(document.fullscreenElement || document.body);
    document.addEventListener('fullscreenchange', update);
    return () => document.removeEventListener('fullscreenchange', update);
  }, []);

  // Tableau : il vole vers la ligne écrite et, tant que la plume ✍️ avance, il écrit lui-même.
  useEffect(() => {
    let element: HTMLElement | null = null;
    let frame = 0, deadline = 0;
    const same = (a: DOMRect, b: DOMRect) => Math.abs(a.x - b.x) < .5 && Math.abs(a.y - b.y) < .5 && Math.abs(a.width - b.width) < .5 && Math.abs(a.height - b.height) < .5;
    const track = () => {
      if (!element?.isConnected) { setFocus(null); return; }
      const bounds = element.getBoundingClientRect();
      const now = performance.now();
      const visible = bounds.width > 0 && bounds.height > 0 && bounds.bottom > 0 && bounds.top < innerHeight;
      const penBounds = element.querySelector<HTMLElement>('.live-pen')?.getBoundingClientRect();
      const writing = !!penBounds && penBounds.width > 0;
      // Une ligne longue peut s'écrire plus de 6,5 s : tant que la plume avance, il la garde en main.
      if (writing) deadline = Math.max(deadline, now + 2000);
      if (now > deadline) { element = null; setFocus(null); return; }
      const rect = writing ? new DOMRect(penBounds!.left - 2, penBounds!.top + penBounds!.height * 0.55, 4, 4) : bounds;
      if (visible) {
        const point = writing ? { x: rect.left, y: rect.top } : { x: bounds.right - 14, y: bounds.top + bounds.height / 2 };
        fly(reachPosition(point, writing, rig.current));
        aimSide(point);
      }
      setFocus(previous => !visible ? null : previous && previous.writing === writing && same(previous.rect, rect) ? previous : { rect, writing });
      frame = requestAnimationFrame(track);
    };
    const receive = (event: Event) => {
      cancelAnimationFrame(frame);
      const candidate = (event as CustomEvent<unknown>).detail;
      element = candidate instanceof HTMLElement && candidate.isConnected ? candidate : null;
      if (!element) { setFocus(null); return; }
      deadline = performance.now() + 6500;
      track();
    };
    window.addEventListener(PROFESSOR_FOCUS, receive);
    return () => { window.removeEventListener(PROFESSOR_FOCUS, receive); cancelAnimationFrame(frame); };
  }, [fly, aimSide]);

  // Simulation : il vole jusqu'au bouton de la commande, tend l'index et appuie quand elle part.
  useEffect(() => {
    if (!control) return;
    const scene = Array.from(document.querySelectorAll<HTMLElement>('[data-professor-target]'))
      .find(node => node.dataset.professorTarget === control.presetId && node.getBoundingClientRect().width > 0);
    if (!scene) return;
    const button = Array.from(scene.querySelectorAll<HTMLElement>('[data-professor-control]'))
      .find(node => (node.dataset.professorControl || '').split(/\s+/).includes(control.command) && node.getBoundingClientRect().width > 0);
    const element = button ?? scene;
    const update = () => {
      const bounds = element.getBoundingClientRect();
      setFocus({ rect: bounds, writing: false });
      const point = { x: bounds.left + bounds.width / 2, y: bounds.top + bounds.height / 2 };
      fly(reachPosition(point, false, rig.current, scene.getBoundingClientRect()));
      aimSide(point);
    };
    update();
    window.addEventListener('resize', update);
    window.addEventListener('scroll', update, true);
    const pressTimer = window.setTimeout(() => {
      const bounds = element.getBoundingClientRect();
      setPress({ key: control.sequence, x: bounds.left + bounds.width / 2, y: bounds.top + bounds.height / 2 });
    }, PROFESSOR_REACH_MS);
    const timer = window.setTimeout(() => { setFocus(null); setPress(null); }, PROFESSOR_REACH_MS + 2400);
    return () => {
      window.clearTimeout(timer); window.clearTimeout(pressTimer);
      window.removeEventListener('resize', update);
      window.removeEventListener('scroll', update, true);
      setFocus(null);
    };
  }, [control, fly, aimSide]);

  // Laboratoire HTML dans une iframe : il vole jusqu'au bouton de la commande, que le laboratoire localise
  // lui-même (`simulation_locate` → `simulation_control_rect`, en px de l'iframe, remis à l'échelle de la
  // page), appuie, et la commande part alors vers l'iframe. Sans réponse, il vise l'iframe entière.
  useEffect(() => {
    if (!labControl) return;
    const iframe = document.querySelector<HTMLIFrameElement>('iframe[title="Simulation"]');
    const deliver = () => {
      if (deliveredLab.current === labControl.sequence) return;
      deliveredLab.current = labControl.sequence;
      iframe?.contentWindow?.postMessage(labControl.message, '*');
    };
    if (!iframe?.contentWindow || minimized || animationFailed) { deliver(); return; }
    let inner: { x: number; y: number; width: number; height: number } | null = null;
    const bounds = () => {
      const frame = iframe.getBoundingClientRect();
      const scale = iframe.clientWidth ? frame.width / iframe.clientWidth : 1;
      return inner
        ? new DOMRect(frame.left + inner.x * scale, frame.top + inner.y * scale, inner.width * scale, inner.height * scale)
        : frame;
    };
    const update = () => {
      const rect = bounds();
      setFocus({ rect, writing: false });
      const point = { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
      fly(reachPosition(point, false, rig.current, iframe.getBoundingClientRect()));
      aimSide(point);
    };
    const onRect = (event: MessageEvent) => {
      const data = event.data as { type?: string; sequence?: number; rect?: { x: number; y: number; width: number; height: number } | null } | null;
      if (event.source !== iframe.contentWindow || data?.type !== 'simulation_control_rect' || data.sequence !== labControl.sequence) return;
      if (data.rect && data.rect.width > 0) { inner = data.rect; update(); }
    };
    window.addEventListener('message', onRect);
    iframe.contentWindow.postMessage({ type: 'simulation_locate', command: labControl.command, parameters: labControl.message.parameters ?? {}, sequence: labControl.sequence }, '*');
    update();
    window.addEventListener('resize', update);
    window.addEventListener('scroll', update, true);
    const pressTimer = window.setTimeout(() => {
      const rect = bounds();
      setPress({ key: -labControl.sequence, x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 });
      deliver();
    }, PROFESSOR_REACH_MS);
    const timer = window.setTimeout(() => { setFocus(null); setPress(null); }, PROFESSOR_REACH_MS + 2400);
    return () => {
      window.clearTimeout(timer); window.clearTimeout(pressTimer);
      window.removeEventListener('message', onRect);
      window.removeEventListener('resize', update);
      window.removeEventListener('scroll', update, true);
      deliver();                                   // une commande suivante ne doit jamais faire perdre celle-ci
      setFocus(null);
    };
  }, [labControl, minimized, animationFailed, fly, aimSide]);

  // Sans rien à montrer, il retourne à sa place (après un court délai, pour enchaîner deux lignes sans aller-retour).
  useEffect(() => {
    if (focus) return;
    const timer = window.setTimeout(() => fly(home.current), RETURN_HOME_MS);
    return () => window.clearTimeout(timer);
  }, [focus, fly]);

  const target = focus?.rect ?? null;
  const writing = !!focus?.writing;
  const aimPoint = useMemo(() => target ? { x: target.left + target.width / 2, y: target.top + target.height / 2 } : null, [target]);
  const end = target && hand ? { x: Math.max(target.left + 4, Math.min(hand.x, target.right - 4)), y: Math.max(target.top + 4, Math.min(hand.y, target.bottom - 4)) } : null;
  const active = !minimized && !animationFailed;

  return createPortal(
    <>
      {end && hand && active && <svg className={`moalim-pointer${writing ? ' moalim-pointer--chalk' : ''}`} aria-hidden="true">
        <line x1={hand.x} y1={hand.y} x2={end.x} y2={end.y} />
        <circle cx={end.x} cy={end.y} r="5" />
      </svg>}
      {target && !writing && <div className={`moalim-target${target.height < 60 ? ' moalim-target--small' : ''}`} aria-hidden="true" style={{ left: target.left, top: target.top, width: target.width, height: target.height }}>
        <span>☞ Moalim</span>
      </div>}
      {press && active && <span key={press.key} className="moalim-press" aria-hidden="true" style={{ left: press.x, top: press.y }} />}
      {sparks.length > 0 && <div className="moalim-sparks" aria-hidden="true">
        {sparks.map(spark => <span key={spark.id} style={{ left: spark.x, top: spark.y, fontSize: spark.size, animationDelay: `${spark.delay}s`, '--dx': `${spark.dx}px` } as CSSProperties}>{spark.emoji}</span>)}
      </div>}
      <div ref={box} className="moalim-avatar" data-state={state} data-minimized={minimized} data-writing={writing && active}
        style={{ transform: `translate(${initial.x}px, ${initial.y}px)` }}>
        {!minimized && (!animationFailed
          ? <Suspense fallback={<img className="moalim-avatar__image" src="/media/avatar/moalim-professeur.png" alt="Chargement de Moalim" />}>
              <Professor3D mood={state} pointing={!!target && !minimized} pointingSide={side} target={aimPoint} writing={writing}
                motion={motion} onHandPosition={onHandPosition} onRig={onRig} gesture={gesture} onError={onAnimationError} />
            </Suspense>
          : <img className="moalim-avatar__image" src="/media/avatar/moalim-professeur.png" alt="Moalim, ton professeur virtuel" draggable={false} />)}
        <div className="moalim-avatar__toolbar">
          <button type="button" className="moalim-avatar__handle" aria-label="Moalim : appuyer pour le saluer, glisser ou touches fléchées pour le déplacer"
            onPointerDown={event => {
              if (event.button !== 0) return;
              event.currentTarget.setPointerCapture(event.pointerId);
              drag.current = { x: event.clientX, y: event.clientY, left: goal.current.x, top: goal.current.y };
            }}
            onPointerMove={event => {
              if (!drag.current) return;
              home.current = clampPosition(drag.current.left + event.clientX - drag.current.x, drag.current.top + event.clientY - drag.current.y);
              fly(home.current, true);
            }}
            onPointerUp={event => {
              const start = drag.current; drag.current = null;
              // Un simple appui sur sa poignée, sans le déplacer : il salue l'élève.
              if (start && Math.hypot(event.clientX - start.x, event.clientY - start.y) < 4) express('greet', Date.now());
            }}
            onPointerCancel={() => { drag.current = null; }}
            onLostPointerCapture={() => { drag.current = null; }}
            onKeyDown={event => {
              const directions: Record<string, [number, number]> = { ArrowLeft: [-20, 0], ArrowRight: [20, 0], ArrowUp: [0, -20], ArrowDown: [0, 20] };
              const delta = directions[event.key];
              if (!delta) return;
              event.preventDefault();
              home.current = clampPosition(goal.current.x + delta[0], goal.current.y + delta[1]);
              fly(home.current);
            }}>⠿ Moalim</button>
          <button type="button" onClick={() => setMinimized(value => !value)} aria-label={minimized ? 'Afficher Moalim' : 'Réduire Moalim'}>{minimized ? '+' : '−'}</button>
        </div>
        <p className="moalim-avatar__status" role="status">{animationFailed ? 'Animation indisponible · portrait affiché' : status}</p>
      </div>
    </>, portalRoot,
  );
}
