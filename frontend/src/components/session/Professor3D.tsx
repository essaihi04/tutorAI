import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { sampleAvatarAudio } from '../../services/avatarAudio';
import { SyllableEnvelope } from '../../services/syllableEnvelope';
import type { ProfessorGestureKind } from '../../services/professorEmotion';

/**
 * Professeur Moalim : personnage rigué aux os humanoïdes standard (Hips, Head, LeftArm, RightHandIndex1…).
 *
 * - Le modèle est recentré et cadré automatiquement, quelle que soit sa taille.
 * - `Idle` tourne en boucle ; pendant la parole, `Talking` prend le relais en fondu. Sans clip
 *   `Talking`, des gestes d'explication sont ajoutés sur les avant-bras, les mains et la tête.
 * - La voix soulève la moustache (os `Moustache`) ; la réflexion lève les sourcils (`Brow*`).
 * - En parlant, les bras expliquent : mains ouvertes, index levé pour un point clé, balayage.
 * - Quand l'élève parle ou écrit, il écoute : tête penchée, buste en avant, hochements, main
 *   derrière l'oreille au début.
 * - Pour montrer un élément, le bras se tend réellement vers lui et l'index se déplie, les autres
 *   doigts se replient ; la position du bout de l'index sert d'origine à la ligne de pointage.
 * - Si le modèle porte des formes faciales (jawOpen, viseme_*, eyeBlink*), la bouche suit la voix.
 */
export type ProfessorMood = 'idle' | 'speaking' | 'thinking' | 'listening';
/** Vitesse du vol à l'écran (px/s), partagée par l'enveloppe sans re-rendu. */
export interface ProfessorMotion { vx: number; vy: number; }
/** Mesures du personnage dans la boîte de 180 × 260 px : épaules et longueur du bras tendu. */
export interface ProfessorRig { shoulderRight: { x: number; y: number }; shoulderLeft: { x: number; y: number }; reach: number; }
interface Props {
  mood: ProfessorMood;
  pointing: boolean;
  /** Côté de l'écran où se trouve la cible, par rapport au professeur. */
  pointingSide: 'left' | 'right';
  /** Point visé, en pixels de la fenêtre. */
  target: { x: number; y: number } | null;
  /** La main tient la plume du tableau : petit mouvement d'écriture. */
  writing?: boolean;
  motion?: { current: ProfessorMotion };
  onHandPosition: (point: { x: number; y: number }) => void;
  onRig?: (rig: ProfessorRig) => void;
  /** Geste d'émotion à jouer (coucou, bras levés, mains sur le cœur, hochement) ; `key` relance le geste. */
  gesture?: { kind: ProfessorGestureKind; key: number } | null;
  onError: () => void;
}
/** Durée de chaque geste d'émotion, en secondes. */
const GESTURE_LENGTH: Record<ProfessorGestureKind, number> = { wave: 2.4, cheer: 1.8, heart: 2.2, nod: 1.2, laugh: 1.8, startle: 1.4 };
const smooth = (a: number, b: number, x: number) => { const t = THREE.MathUtils.clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
export const PROFESSOR_MODEL_URL = '/media/avatar/moalim-professeur.glb';
const VIEW_WIDTH = 180, VIEW_HEIGHT = 260;
/** Le canevas déborde de la boîte de chaque côté : un bras tendu n'est jamais coupé. */
const CANVAS_MARGIN = 120, CANVAS_WIDTH = VIEW_WIDTH + 2 * CANVAS_MARGIN;
const CAMERA_FOV = 30;
/** Ouverture maximale (radians) de la moustache et petit mouvement du nez qui la porte. */
const MOUSTACHE_OPEN = 0.55, NOSE_OPEN = 0.12;
/** Taille de la moustache : à 1, ses pointes dépassent un peu des joues. */
const MOUSTACHE_SCALE = 0.85;
/** Marge autour du personnage dans le cadre. */
const FRAME_MARGIN = 1.12;
const FINGERS = ['Index', 'Middle', 'Ring', 'Pinky'] as const;

export default function Professor3D({ mood, pointing, pointingSide, target, writing = false, motion, onHandPosition, onRig, gesture, onError }: Props) {
  const gestureRef = useRef(gesture);
  useEffect(() => { gestureRef.current = gesture; }, [gesture]);
  const host = useRef<HTMLDivElement>(null);
  const moodRef = useRef(mood), pointRef = useRef(pointing), sideRef = useRef(pointingSide), targetRef = useRef(target), writingRef = useRef(writing);
  const motionRef = useRef(motion);
  const onRigRef = useRef(onRig);
  useEffect(() => { onRigRef.current = onRig; }, [onRig]);
  useEffect(() => { writingRef.current = writing; }, [writing]);
  useEffect(() => { motionRef.current = motion; }, [motion]);
  useEffect(() => { moodRef.current = mood; }, [mood]);
  useEffect(() => { pointRef.current = pointing; }, [pointing]);
  useEffect(() => { sideRef.current = pointingSide; }, [pointingSide]);
  useEffect(() => { targetRef.current = target; }, [target]);

  useEffect(() => {
    const container = host.current;
    if (!container) return;
    let renderer: THREE.WebGLRenderer;
    try { renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true }); }
    catch { onError(); return; }
    renderer.setSize(CANVAS_WIDTH, VIEW_HEIGHT);
    Object.assign(renderer.domElement.style, { position: 'absolute', left: `-${CANVAS_MARGIN}px`, top: '0', pointerEvents: 'none' });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setClearColor(0, 0);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    container.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(CAMERA_FOV, CANVAS_WIDTH / VIEW_HEIGHT, 0.01, 50);
    camera.position.set(0, 1, 3); camera.lookAt(0, 1, 0);
    scene.add(new THREE.HemisphereLight(0xffffff, 0x6b7280, 1.6));
    const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(-1.5, 2.8, 2.6); scene.add(key);
    const fill = new THREE.DirectionalLight(0xdbe4ff, 0.9); fill.position.set(1.8, 1.6, 2); scene.add(fill);
    const rim = new THREE.DirectionalLight(0xffffff, 0.8); rim.position.set(0, 2.4, -2.5); scene.add(rim);

    let disposed = false, frame = 0;
    let model: THREE.Object3D | null = null;
    let mixer: THREE.AnimationMixer | null = null;
    let idleAction: THREE.AnimationAction | null = null, talkAction: THREE.AnimationAction | null = null;
    /** Mélange Idle → Talking (0…1) et dernier instant de parole, pour ne pas rebasculer entre deux phrases. */
    let talkBlend = 0, lastSpoke = -10;
    /** Cible lissée du pointage, gardée pendant que le bras redescend. */
    let aimGoal: { x: number; y: number } | null = null;
    const bones = new Map<string, THREE.Bone>();
    /** Dernière pose écrite par le mixeur pour chaque os (pose de référence pour les os sans piste). */
    const rest = new Map<THREE.Bone, { q: THREE.Quaternion; p: THREE.Vector3; s: THREE.Vector3 }>();
    const remember = () => { for (const [b, pose] of rest) { pose.q.copy(b.quaternion); pose.p.copy(b.position); pose.s.copy(b.scale); } };
    const faces: THREE.Mesh[] = [];
    const clock = new THREE.Clock();
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let speech = 0, talk = 0, think = 0, listen = 0, aim = 0, lean = 0, rise = 0, scribe = 0;
    /** Début de l'écoute en cours (la main va derrière l'oreille un instant) ; taille du personnage. */
    let listenStart = -10, height = 1;
    const syllables = new SyllableEnvelope();
    let aimSide: 'Left' | 'Right' = 'Right';
    let gesturePlayed = 0, gestureStart = -10, gestureKind: ProfessorGestureKind | null = null;
    /** Regard (−1…1, x vers la droite de l'écran, y vers le bas) et coups d'œil de temps en temps. */
    let gazeX = 0, gazeY = 0, gazeGoalX = 0, gazeGoalY = 0, glanceX = 0, glanceY = 0, glanceEnd = 0, nextGlance = 2;
    /** Dernière position de la souris : il la suit des yeux pendant quelques secondes après chaque mouvement. */
    let mouse: { x: number; y: number; at: number } | null = null;
    const MOUSE_FOLLOW_S = 8;
    const onPointerMove = (event: PointerEvent) => { mouse = { x: event.clientX, y: event.clientY, at: clock.elapsedTime }; };
    window.addEventListener('pointermove', onPointerMove, { passive: true });
    let nextBlink = 2.5, blinkStarted = -10, blinkCount = 0;
    const vA = new THREE.Vector3(), vB = new THREE.Vector3(), vC = new THREE.Vector3(), vD = new THREE.Vector3();
    const qA = new THREE.Quaternion(), qB = new THREE.Quaternion(), qId = new THREE.Quaternion();
    const X = new THREE.Vector3(1, 0, 0), Y = new THREE.Vector3(0, 1, 0), Z = new THREE.Vector3(0, 0, 1);
    const plane = new THREE.Plane(), ray = new THREE.Ray();

    function disposeModel(root: THREE.Object3D) {
      root.traverse(object => {
        if (!(object instanceof THREE.Mesh)) return;
        object.geometry.dispose();
        for (const material of Array.isArray(object.material) ? object.material : [object.material]) {
          for (const value of Object.values(material)) if (value instanceof THREE.Texture) value.dispose();
          material.dispose();
        }
      });
    }
    const bone = (name: string) => bones.get(name);

    /** Rotation d'un os autour d'un axe exprimé dans le repère du monde. */
    function rotateWorld(b: THREE.Bone | undefined, axis: THREE.Vector3, angle: number) {
      if (!b || !angle) return;
      b.parent!.getWorldQuaternion(qB);
      qA.setFromAxisAngle(axis, angle);
      b.quaternion.premultiply(qB.clone().invert().multiply(qA).multiply(qB));
      b.updateMatrixWorld(true);
    }
    /** Déplace un os verticalement (mètres, repère du monde), par exemple pour la respiration. */
    function liftWorld(b: THREE.Bone | undefined, dy: number) {
      if (!b || !dy) return;
      b.parent!.getWorldQuaternion(qB); b.parent!.getWorldScale(vD);
      b.position.add(vC.set(0, dy / (vD.y || 1), 0).applyQuaternion(qB.invert()));
      b.updateMatrixWorld(true);
    }
    /** Fait tourner l'os pour que le segment os → enfant pointe vers `goal`, avec un poids 0…1. */
    function aimSegment(b: THREE.Bone | undefined, child: THREE.Bone | undefined, goal: THREE.Vector3, weight: number) {
      if (!b || !child || weight <= 0) return;
      b.getWorldPosition(vA); child.getWorldPosition(vB);
      const current = vB.sub(vA).normalize();
      const wanted = vC.copy(goal).sub(vA).normalize();
      qA.setFromUnitVectors(current, wanted);
      qA.slerp(qId, 1 - weight);
      b.parent!.getWorldQuaternion(qB);
      b.quaternion.premultiply(qB.clone().invert().multiply(qA).multiply(qB));
      b.updateMatrixWorld(true);
    }
    /** Replie (angle > 0) ou déplie un doigt autour de l'axe de flexion de la main. */
    function curlFinger(side: 'Left' | 'Right', finger: string, angle: number) {
      const hand = bone(`${side}Hand`), index1 = bone(`${side}HandIndex1`), pinky1 = bone(`${side}HandPinky1`);
      if (!hand || !index1 || !pinky1 || !angle) return;
      hand.getWorldPosition(vA); index1.getWorldPosition(vB); pinky1.getWorldPosition(vC);
      const across = vD.copy(vB).sub(vC).normalize();              // de l'auriculaire vers l'index
      const along = vB.sub(vA).normalize();                          // du poignet vers les doigts
      const flexAxis = across.clone().cross(along).cross(along).normalize().negate();
      const axis = side === 'Right' ? flexAxis : flexAxis.negate();
      for (const k of [1, 2, 3]) rotateWorld(bone(`${side}Hand${finger}${k}`), axis, angle * (k === 1 ? 0.8 : 1));
    }

    /** Recentre le personnage (pieds au sol, axe vertical au centre) et cadre la caméra sur lui. */
    function frameModel(root: THREE.Object3D) {
      root.updateMatrixWorld(true);
      const box = new THREE.Box3();
      root.traverse(object => {
        if (object instanceof THREE.SkinnedMesh) { object.computeBoundingBox(); box.union(object.boundingBox!.clone().applyMatrix4(object.matrixWorld)); }
        else if (object instanceof THREE.Mesh) box.expandByObject(object);
      });
      const size = box.getSize(new THREE.Vector3()), centre = box.getCenter(new THREE.Vector3());
      root.position.x -= centre.x; root.position.z -= centre.z; root.position.y -= box.min.y;
      root.updateMatrixWorld(true);
      height = size.y;
      const half = Math.tan(THREE.MathUtils.degToRad(CAMERA_FOV / 2));
      const distance = Math.max(size.y * FRAME_MARGIN / 2 / half, size.x * FRAME_MARGIN / 2 / (half * VIEW_WIDTH / VIEW_HEIGHT)) + size.z / 2;
      camera.position.set(0, size.y / 2, distance);
      camera.lookAt(0, size.y / 2, 0);
      camera.updateMatrixWorld(true);
      // Mesures transmises à l'enveloppe : position des épaules et portée du bras, en px de la boîte.
      const pxPerMetre = VIEW_HEIGHT / (2 * (distance - size.z / 2) * half);
      const toBox = (b: THREE.Bone | undefined) => {
        if (!b) return { x: VIEW_WIDTH / 2, y: VIEW_HEIGHT / 3 };
        const p = b.getWorldPosition(new THREE.Vector3()).project(camera);
        return { x: (p.x + 1) / 2 * CANVAS_WIDTH - CANVAS_MARGIN, y: (1 - p.y) / 2 * VIEW_HEIGHT };
      };
      const length = (...names: string[]) => names.slice(1).reduce((sum, name, i) => {
        const a = bone(names[i]), b = bone(name);
        return a && b ? sum + a.getWorldPosition(new THREE.Vector3()).distanceTo(b.getWorldPosition(new THREE.Vector3())) : sum;
      }, 0);
      const arm = length('RightArm', 'RightForeArm', 'RightHand', 'RightHandIndex1', 'RightHandIndex3') * 1.1;
      onRigRef.current?.({ shoulderRight: toBox(bone('RightArm')), shoulderLeft: toBox(bone('LeftArm')), reach: Math.max(40, arm * pxPerMetre) });
    }

    function screenToWorld(point: { x: number; y: number }, anchor: THREE.Vector3, out: THREE.Vector3) {
      const bounds = renderer.domElement.getBoundingClientRect();
      const ndcX = THREE.MathUtils.clamp(((point.x - bounds.left) / bounds.width) * 2 - 1, -4, 4);
      const ndcY = THREE.MathUtils.clamp(-(((point.y - bounds.top) / bounds.height) * 2 - 1), -4, 4);
      vD.set(ndcX, ndcY, 0.5).unproject(camera);
      ray.origin.copy(camera.position); ray.direction.copy(vD.sub(camera.position).normalize());
      camera.getWorldDirection(vD);
      plane.setFromNormalAndCoplanarPoint(vD, anchor);
      return ray.intersectPlane(plane, out);
    }

    new GLTFLoader().load(PROFESSOR_MODEL_URL, gltf => {
      if (disposed) { disposeModel(gltf.scene); return; }
      model = gltf.scene;
      model.traverse(object => {
        if (object instanceof THREE.Bone) {
          bones.set(object.name.replace(/^mixamorig:?/, ''), object);
          rest.set(object, { q: object.quaternion.clone(), p: object.position.clone(), s: object.scale.clone() });
        }
        if (object instanceof THREE.Mesh) {
          object.frustumCulled = false;
          if (object.morphTargetDictionary && Object.keys(object.morphTargetDictionary).length) faces.push(object);
        }
      });
      if (!bones.has('Head') || !bones.has('RightArm') || !bones.has('LeftArm')) { disposeModel(model); model = null; onError(); return; }
      scene.add(model);
      mixer = new THREE.AnimationMixer(model);
      const idle = gltf.animations.find(clip => /idle/i.test(clip.name)) ?? gltf.animations[0];
      const talking = gltf.animations.find(clip => /talk/i.test(clip.name));
      if (idle) { idleAction = mixer.clipAction(idle); idleAction.play(); }
      if (talking) { talkAction = mixer.clipAction(talking); talkAction.setEffectiveWeight(0); talkAction.play(); }
      mixer.update(0);
      remember();
      frameModel(model);
      container.dataset.ready = 'true';
    }, undefined, () => { if (!disposed) onError(); });

    function render() {
      if (disposed) return;
      const delta = Math.min(clock.getDelta(), 0.1);
      const time = clock.elapsedTime;
      const ease = (k: number) => 1 - Math.exp(-delta * k);
      const { weights, amplitude, rms, latency } = sampleAvatarAudio();
      // Gestes d'émotion : enveloppe d'entrée/sortie en douceur ; `key` relance le geste.
      const wantedGesture = gestureRef.current;
      if (wantedGesture && wantedGesture.key !== gesturePlayed) { gesturePlayed = wantedGesture.key; gestureKind = wantedGesture.kind; gestureStart = time; }
      const gestureAge = time - gestureStart, gestureLength = gestureKind ? GESTURE_LENGTH[gestureKind] : 0;
      const env = gestureKind && gestureAge < gestureLength ? smooth(0, 0.35, gestureAge) * smooth(0, 0.45, gestureLength - gestureAge) : 0;
      // Ouverture syllabe par syllabe, retardée de la latence de sortie : elle tombe avec le son entendu.
      // Un rire fait trembler la moustache même sans voix.
      const laughMouth = gestureKind === 'laugh' ? env * (0.45 + 0.55 * Math.abs(Math.sin(time * 11))) : 0;
      const mouth = Math.max(syllables.push(rms, delta, time, latency), laughMouth);
      const speaking = moodRef.current === 'speaking';
      speech += (Math.min(1, amplitude * 4) - speech) * ease(4);
      talk += ((speaking ? 1 : 0) - talk) * ease(2.5);
      think += ((moodRef.current === 'thinking' ? 1 : 0) - think) * ease(2.5);
      const listening = moodRef.current === 'listening';
      if (listening && listen < 0.05) listenStart = time;
      listen += ((listening ? 1 : 0) - listen) * ease(3);
      const pointingNow = pointRef.current && !!targetRef.current;
      if (pointingNow && aim < 0.05) aimSide = sideRef.current === 'right' ? 'Left' : 'Right';   // il lui fait face : sa gauche est à droite de l'écran
      aim += ((pointingNow ? 1 : 0) - aim) * ease(5);
      const flight = motionRef.current?.current;
      // Seul un vrai vol penche le corps et fait traîner les jambes : en suivant la plume au tableau, il glisse
      // lentement, et sans ce seuil ses jambes se pliaient et se dépliaient sans arrêt.
      const vx = flight?.vx ?? 0, speedPx = Math.hypot(vx, flight?.vy ?? 0), flying = THREE.MathUtils.clamp((speedPx - 180) / 500, 0, 1);
      lean += (THREE.MathUtils.clamp(vx / 700, -1, 1) * flying - lean) * ease(4);
      rise += (flying - rise) * ease(4);
      scribe += ((writingRef.current ? 1 : 0) - scribe) * ease(6);

      if (mixer && model) {
        mixer.timeScale = reducedMotion.matches ? 0.3 : 1;
        // Parole : fondu vers l'animation de parole du modèle quand elle existe.
        // Parole : mélange progressif des deux animations, qui tournent en continu. L'ancien fondu
        // (reset + crossFade suivi de setEffectiveWeight, qui annule le fondu) faisait sauter les bras d'une
        // pose à l'autre à chaque début et fin de phrase ; une pause de moins de 0,8 s ne rebascule pas.
        if (speaking) lastSpoke = time;
        if (talkAction && idleAction) {
          talkBlend += ((time - lastSpoke < 0.8 ? 1 : 0) - talkBlend) * ease(3);
          talkAction.setEffectiveWeight(talkBlend);
          idleAction.setEffectiveWeight(1 - talkBlend);
        }
        // Les rotations ajoutées ci-dessous ne doivent pas s'accumuler d'une image à l'autre : chaque os
        // repart de la dernière pose écrite par le mixeur. Surtout pas de la pose de référence (bras en
        // croix) : three.js ne réécrit un os que si sa valeur animée change, et pendant une pose tenue
        // l'os restait alors en croix, d'où des bras et des mains qui sautaient par à-coups.
        for (const [b, pose] of rest) { b.quaternion.copy(pose.q); b.position.copy(pose.p); b.scale.copy(pose.s); }
        mixer.update(delta);
        remember();
        model.updateMatrixWorld(true);
        // Voix : la moustache se soulève et retombe avec chaque syllabe ; les sourcils suivent la réflexion.
        const moustache = bone('Moustache');
        // Rotation autour de l'axe gauche-droite du monde (il fait face à +Z) : un point situé devant et
        // sous le pivot remonte pour un angle négatif, quel que soit le repère local de l'os.
        rotateWorld(bone('Nose'), X, -mouth * NOSE_OPEN);
        if (moustache) {
          rotateWorld(moustache, X, -mouth * MOUSTACHE_OPEN);
          moustache.scale.multiplyScalar(MOUSTACHE_SCALE);                               // remise à la taille de repos à chaque image
          moustache.updateMatrixWorld(true);
        }
        // Sourcils : un seul se lève quand il réfléchit, les deux accompagnent les syllabes appuyées.
        rotateWorld(bone('BrowLeft'), X, -(think * 0.45 + speech * 0.12 + mouth * 0.06));
        rotateWorld(bone('BrowRight'), X, -(think * 0.15 + speech * 0.12 + mouth * 0.06));
        if (!reducedMotion.matches) {
          // Gestes d'explication : fenêtres alternées, avec des pauses, plus amples quand la voix porte.
          // Chaque fenêtre (3 s, enveloppe sin²) porte un geste : mains ouvertes, index levé (un point clé) ou
          // balayage. Le geste change seulement entre deux fenêtres, quand le bras est revenu : jamais de saut.
          const GESTURE_WINDOW = 3;
          const beat = (period: number, offset: number) => { const p = (time + offset) % period; return p < GESTURE_WINDOW ? Math.sin(Math.PI * p / GESTURE_WINDOW) ** 2 : 0; };
          const phase = (period: number, offset: number) => ((time + offset) % period) / GESTURE_WINDOW;
          const kindOf = (period: number, offset: number) => (['open', 'point', 'sweep', 'open', 'sweep', 'point'] as const)[Math.floor((time + offset) / period) % 6];
          // Le clip Talking garde les bras immobiles : gestes de mains procéduraux, francs quand il explique
          // sans rien montrer ni écrire, plus discrets pour le bras libre pendant un pointage ou l'écriture.
          const procedural = talkAction ? (aim > 0.02 || scribe > 0.02 ? 0.3 : 0.85) : 1;
          const voiced = 0.6 + 0.4 * speech;
          const gestureR = procedural * talk * voiced * beat(4.7, 0.3);
          const gestureL = procedural * talk * voiced * beat(5.6, 3.1);
          const both = procedural * talk * 0.3;
          // Respiration : la tête et les épaules se soulèvent doucement.
          const breath = (1 - Math.cos(time * 1.4)) / 2;
          liftWorld(bone('Head'), breath * 0.006);
          for (const shoulder of ['LeftShoulder', 'RightShoulder']) liftWorld(bone(shoulder), breath * 0.004);
          // Gestes d'émotion : coucou, bras levés, mains sur le cœur, hochement, rire, sursaut.
          // Le bras qui pointe ou écrit n'est jamais emprunté.
          if (env > 0.001 && gestureKind) {
            const free = (side: 'Left' | 'Right') => !(aim > 0.02 && side === aimSide);
            if (gestureKind === 'wave') {
              const side = free('Left') ? 'Left' : 'Right', sign = side === 'Left' ? 1 : -1;
              rotateWorld(bone(`${side}Arm`), Z, sign * env * 1.35);                            // bras levé sur le côté
              rotateWorld(bone(`${side}ForeArm`), Z, sign * env * 1.1);
              rotateWorld(bone(`${side}Hand`), Z, sign * env * 0.55 * Math.sin(time * 9));      // la main salue
              rotateWorld(bone('Head'), Z, -sign * env * 0.1);
            } else if (gestureKind === 'cheer') {
              for (const [side, sign] of [['Left', 1], ['Right', -1]] as const) {
                if (!free(side)) continue;
                rotateWorld(bone(`${side}Arm`), Z, sign * env * 1.5);                           // les deux bras en V
                rotateWorld(bone(`${side}ForeArm`), Z, sign * env * (0.8 + 0.15 * Math.sin(time * 8)));
                for (const finger of FINGERS) curlFinger(side, finger, -env * 0.2);
              }
              liftWorld(bone('Hips'), env * 0.05 * Math.max(0, Math.sin(time * 7)));            // petit saut de joie
            } else if (gestureKind === 'heart') {
              for (const [side, sign] of [['Left', 1], ['Right', -1]] as const) {
                if (!free(side)) continue;
                rotateWorld(bone(`${side}Arm`), X, -env * 0.8);                                  // mains ramenées sur le cœur
                rotateWorld(bone(`${side}Arm`), Z, -sign * env * 0.2);
                rotateWorld(bone(`${side}ForeArm`), X, -env * 1.7);
                rotateWorld(bone(`${side}ForeArm`), Y, sign * env * 0.7);
                for (const finger of FINGERS) curlFinger(side, finger, env * 0.4);
              }
              rotateWorld(bone('Head'), Z, env * 0.14);
              for (const brow of ['BrowLeft', 'BrowRight']) rotateWorld(bone(brow), X, -env * 0.2);
            } else if (gestureKind === 'nod') {
              rotateWorld(bone('Head'), X, env * 0.16 * Math.max(0, Math.sin(time * 7)));       // deux hochements
            } else if (gestureKind === 'laugh') {
              const shake = Math.abs(Math.sin(time * 11));
              liftWorld(bone('Hips'), env * 0.03 * shake);                                       // le corps saute
              for (const shoulder of ['LeftShoulder', 'RightShoulder']) liftWorld(bone(shoulder), env * 0.012 * shake);
              rotateWorld(bone('Head'), X, -env * (0.14 - 0.06 * shake));                        // tête en arrière, secouée
              rotateWorld(bone('Head'), Z, env * 0.08 * Math.sin(time * 5.5));
              for (const brow of ['BrowLeft', 'BrowRight']) rotateWorld(bone(brow), X, -env * 0.25);
            } else if (gestureKind === 'startle') {
              rotateWorld(bone('Head'), X, -env * 0.2);                                           // tête en arrière
              for (const brow of ['BrowLeft', 'BrowRight']) rotateWorld(bone(brow), X, -env * 0.55);   // sourcils très hauts
              for (const [side, sign] of [['Left', 1], ['Right', -1]] as const) {
                if (!free(side)) continue;
                rotateWorld(bone(`${side}Arm`), Z, sign * env * 0.55);                          // mains levées, ouvertes
                rotateWorld(bone(`${side}ForeArm`), X, -env * 1.3);
                for (const finger of FINGERS) curlFinger(side, finger, -env * 0.3);
              }
              liftWorld(bone('Hips'), env * 0.03 * smooth(0, 0.2, gestureAge) * (1 - smooth(0.3, 0.7, gestureAge)));   // un sursaut
            }
          }
          // Écoute : tête penchée, buste un peu en avant, sourcils levés, petits hochements réguliers ; au début,
          // la main libre va derrière l'oreille (« je t'écoute »), puis redescend.
          const earSide: 'Left' | 'Right' = aim > 0.02 && aimSide === 'Left' ? 'Right' : 'Left';
          const listenAge = time - listenStart;
          const cup = listen * smooth(0.1, 0.7, listenAge) * (1 - smooth(2.4, 3.2, listenAge));
          if (listen > 0.001) {
            rotateWorld(bone('Head'), Z, (earSide === 'Left' ? -1 : 1) * listen * 0.14);      // penche l'oreille vers l'élève
            rotateWorld(bone('Spine'), X, listen * 0.07);
            const nodPhase = (time + 0.4) % 2.6;
            rotateWorld(bone('Head'), X, listen * 0.09 * (nodPhase < 0.8 ? Math.sin(Math.PI * nodPhase / 0.8) ** 2 : 0));
            for (const brow of ['BrowLeft', 'BrowRight']) rotateWorld(bone(brow), X, -listen * 0.18);
          }
          if (cup > 0.001) {
            const head = bone('Head'), shoulder = bone(`${earSide}Arm`), elbow = bone(`${earSide}ForeArm`), hand = bone(`${earSide}Hand`);
            if (head && shoulder && elbow && hand) {
              const out = earSide === 'Left' ? 1 : -1;                                           // sa gauche est à droite de l'écran
              head.getWorldPosition(vA);
              const ear = vA.clone().add(vB.set(out * 0.3 * height, 0.22 * height, 0.02 * height));
              shoulder.getWorldPosition(vA);
              const elbowGoal = vA.clone().add(vB.set(out * 0.2 * height, 0.02 * height, 0.06 * height));
              aimSegment(shoulder, elbow, elbowGoal, cup);
              aimSegment(elbow, hand, ear, cup);
              rotateWorld(hand, Y, -out * cup * 0.6);                                           // paume tournée vers l'avant, en cornet
              for (const finger of FINGERS) curlFinger(earSide, finger, cup * 0.45);
            }
          }
          // Vol : le corps penche dans le sens du déplacement, les jambes traînent derrière.
          rotateWorld(bone('Hips'), Z, -lean * 0.22);
          rotateWorld(bone('Spine'), X, rise * 0.12);
          for (const leg of ['LeftUpLeg', 'RightUpLeg']) rotateWorld(bone(leg), X, -rise * 0.35);
          for (const knee of ['LeftLeg', 'RightLeg']) rotateWorld(bone(knee), X, rise * 0.5);
          rotateWorld(bone('Spine2'), Y, talk * Math.sin(time * 0.9) * 0.05);
          rotateWorld(bone('Head'), X, -talk * (0.03 + speech * 0.05) * Math.sin(time * 2.3) + think * -0.12);
          rotateWorld(bone('Head'), Z, think * 0.12 + talk * Math.sin(time * 0.7) * 0.03);
          for (const [side, g, sign, period, offset] of [['Right', gestureR, -1, 4.7, 0.3], ['Left', gestureL, 1, 5.6, 3.1]] as const) {
            if ((side === aimSide && aim > 0.02) || both + g < 0.001) continue;
            if (side === earSide && cup > 0.02) continue;
            const lift = Math.min(1, both + g);
            const kind = kindOf(period, offset), p = phase(period, offset);
            const pointUp = kind === 'point' ? g : 0;                                         // index levé : un point clé
            const sweep = kind === 'sweep' ? g * Math.sin(Math.PI * 2 * p) : 0;                // la main balaie de dedans en dehors
            rotateWorld(bone(`${side}Arm`), X, -lift * 0.5 - pointUp * 0.25);                 // bras vers l'avant
            rotateWorld(bone(`${side}Arm`), Z, sign * (lift * 0.3 + sweep * 0.32));           // et écarté du corps
            const elbowBone = bone(`${side}ForeArm`);
            rotateWorld(elbowBone, X, -lift * (1.45 + 0.22 * Math.sin(time * 3.1 + (sign > 0 ? 1 : 0))) - pointUp * 0.45);   // main à hauteur de poitrine
            rotateWorld(elbowBone, Y, -sign * (lift * 0.35 + sweep * 0.25));                  // avant-bras ouvert vers l'extérieur
            const handBone = bone(`${side}Hand`);
            if (elbowBone && handBone) {
              elbowBone.getWorldPosition(vA); handBone.getWorldPosition(vB);
              rotateWorld(handBone, vB.sub(vA).normalize(), -sign * (lift - pointUp * 0.8) * 1.1);   // paume vers le haut (de côté pour l'index)
            }
            rotateWorld(handBone, Z, sign * g * 0.3 * Math.sin(time * 2.2) * (1 - pointUp));
            if (kind === 'point') rotateWorld(handBone, X, -pointUp * 0.25 * Math.max(0, Math.sin(time * 6)));   // petits coups d'index
            for (const finger of FINGERS) curlFinger(side, finger, finger === 'Index' ? 0.15 + 0.1 * lift - pointUp * 0.35 : 0.15 + 0.1 * lift + pointUp * 1.1);
            curlFinger(side, 'Thumb', pointUp * 0.5);
          }
          // Pointage réel : épaule puis coude vers la cible, index tendu, autres doigts repliés.
          // La cible glisse vers le nouvel élément au lieu d'y sauter, et reste en place pendant que le bras redescend.
          const wanted = targetRef.current;
          if (wanted) aimGoal = aimGoal && aim > 0.01
            ? { x: aimGoal.x + (wanted.x - aimGoal.x) * ease(9), y: aimGoal.y + (wanted.y - aimGoal.y) * ease(9) }
            : { ...wanted };
          const goal = aimGoal;
          if (aim > 0.01 && goal) {
            const shoulder = bone(`${aimSide}Arm`), elbow = bone(`${aimSide}ForeArm`), hand = bone(`${aimSide}Hand`);
            if (shoulder && screenToWorld(goal, shoulder.getWorldPosition(vA).clone(), vB)) {
              const point = vB.clone();
              point.z += 0.35;                                                                // un peu vers l'élève, pas dans le dos
              rotateWorld(bone('Spine2'), Y, (aimSide === 'Right' ? -1 : 1) * aim * 0.12);
              aimSegment(shoulder, elbow, point, aim);
              aimSegment(elbow, hand, point, aim * 0.9);
              aimSegment(hand, bone(`${aimSide}HandIndex1`), point, aim * 0.6);
              // Écriture : la main serre la plume (doigts repliés) et trace de petites boucles.
              if (scribe > 0.01 && hand) {
                rotateWorld(hand, Z, scribe * 0.18 * Math.sin(time * 11));
                rotateWorld(hand, X, scribe * 0.12 * Math.sin(time * 7.3));
              }
              for (const finger of ['Middle', 'Ring', 'Pinky']) curlFinger(aimSide, finger, aim * (1.2 + scribe * 0.3));
              curlFinger(aimSide, 'Index', -aim * 0.15 + scribe * 0.6);
              curlFinger(aimSide, 'Thumb', scribe * 0.5);
              rotateWorld(bone('Head'), Y, (aimSide === 'Right' ? -1 : 1) * aim * 0.28);                 // le regard suit le bras
            }
          }
          // Regard : vers l'élément montré, en l'air quand il réfléchit, sinon vers l'élève avec un coup
          // d'œil de côté de temps en temps ; un grand changement de direction s'accompagne d'un clignement.
          let goalX = 0, goalY = 0;
          // Direction du regard (−1…1) vers un point de l'écran, depuis la position de la tête à l'écran.
          const lookAtScreen = (px: number, py: number, range: number) => {
            const head = bone('Head');
            if (!head) return;
            head.getWorldPosition(vA).project(camera);
            const bounds = renderer.domElement.getBoundingClientRect();
            const hx = bounds.left + (vA.x + 1) * bounds.width / 2, hy = bounds.top + (1 - vA.y) * bounds.height / 2;
            goalX = THREE.MathUtils.clamp((px - hx) / range, -1, 1);
            goalY = THREE.MathUtils.clamp((py - hy) / range, -1, 1);
          };
          const mouseRecent = mouse && time - mouse.at < MOUSE_FOLLOW_S;
          if (aim > 0.3 && aimGoal) lookAtScreen(aimGoal.x, aimGoal.y, 250);
          else if (mouseRecent) lookAtScreen(mouse!.x, mouse!.y, 300);                       // il suit la souris des yeux
          else if (listen > 0.5) { goalX = 0; goalY = 0.05; }                                 // il regarde l'élève qui parle
          else if (think > 0.5) { goalX = -0.5; goalY = -0.8; }
          else {
            if (time > nextGlance) {
              glanceX = Math.sin(time * 7.9) * 0.7; glanceY = Math.sin(time * 5.3) * 0.3;
              glanceEnd = time + 0.5 + Math.abs(Math.sin(time * 3.3)) * 1.2;
              nextGlance = glanceEnd + 2.5 + Math.abs(Math.sin(time * 2.1)) * 4;
            }
            if (time < glanceEnd) { goalX = glanceX; goalY = glanceY; }
          }
          if (Math.abs(goalX - gazeGoalX) + Math.abs(goalY - gazeGoalY) > 0.6 && time - blinkStarted > 0.6) blinkStarted = time;
          gazeGoalX = goalX; gazeGoalY = goalY;
          gazeX += (goalX - gazeX) * ease(14); gazeY += (goalY - gazeY) * ease(14);
          rotateWorld(bone('Head'), Y, gazeX * 0.16);                                          // la tête accompagne un peu le regard
          rotateWorld(bone('Head'), X, gazeY * 0.1);
        }
      }

      // Visage : actif seulement si le modèle exporte des formes faciales.
      if (time >= nextBlink) { blinkStarted = time; nextBlink = time + 3.1 + (Math.sin(++blinkCount * 2.39) + 1) * 1.8; }
      const blinkAge = time - blinkStarted;
      const blink = blinkAge > 0.2 ? 0 : Math.sin(Math.PI * blinkAge / 0.2);
      const jaw = mouth * 0.6;
      for (const mesh of faces) {
        const dict = mesh.morphTargetDictionary!, influences = mesh.morphTargetInfluences!;
        for (const [name, index] of Object.entries(dict)) {
          if (name.startsWith('viseme_')) influences[index] = weights[name] || 0;
          else if (name === 'jawOpen' || name === 'mouthOpen') influences[index] = jaw;
          else if (name === 'eyeBlinkLeft' || name === 'eyeBlinkRight' || name === 'eyesClosed') influences[index] = blink;
          else if (name === 'lookRight') influences[index] = Math.max(0, gazeX);
          else if (name === 'lookLeft') influences[index] = Math.max(0, -gazeX);
          else if (name === 'lookUp') influences[index] = Math.max(0, -gazeY);
          else if (name === 'lookDown') influences[index] = Math.max(0, gazeY);
          else if (name === 'mouthSmile' || name === 'mouthSmileLeft' || name === 'mouthSmileRight') influences[index] = 0.15;
        }
      }
      container!.dataset.mouth = String(jaw);
      container!.dataset.aim = aim.toFixed(2);
      container!.dataset.gaze = `${gazeX.toFixed(2)} ${gazeY.toFixed(2)}`;
      renderer.render(scene, camera);

      if (pointRef.current) {
        const tip = bone(`${aimSide}HandIndex3`), mid = bone(`${aimSide}HandIndex2`);
        if (tip && mid) {
          tip.getWorldPosition(vA); mid.getWorldPosition(vB);
          vA.add(vA.clone().sub(vB).multiplyScalar(0.9)).project(camera);                    // prolongé jusqu'au bout du doigt
          const bounds = renderer.domElement.getBoundingClientRect();
          onHandPosition({ x: bounds.left + (vA.x + 1) * bounds.width / 2, y: bounds.top + (1 - vA.y) * bounds.height / 2 });
        }
      }
      frame = requestAnimationFrame(render);
    }
    render();
    const lost = (event: Event) => { event.preventDefault(); onError(); };
    renderer.domElement.addEventListener('webglcontextlost', lost);
    return () => {
      disposed = true;
      cancelAnimationFrame(frame);
      window.removeEventListener('pointermove', onPointerMove);
      mixer?.stopAllAction();
      if (model) disposeModel(model);
      renderer.domElement.removeEventListener('webglcontextlost', lost);
      renderer.dispose();
      renderer.domElement.remove();
    };
  }, [onError, onHandPosition]);
  return <div ref={host} className="moalim-avatar__3d" role="img" aria-label="Professeur Moalim animé" />;
}
