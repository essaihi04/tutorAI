import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { sampleAvatarAudio } from '../../services/avatarAudio';

/**
 * Professeur Moalim : avatar Avaturn rigué (squelette humanoïde standard, 52 os dont 30 phalanges).
 *
 * - L'animation de repos fournie par le modèle tourne en boucle (AnimationMixer).
 * - Pendant la parole, des gestes d'explication s'ajoutent sur les avant-bras, les mains et la tête.
 * - Pour montrer un élément, le bras se tend réellement vers lui et l'index se déplie, les autres
 *   doigts se replient ; la position du bout de l'index sert d'origine à la ligne de pointage.
 * - Si le modèle porte des formes faciales (jawOpen, viseme_*, eyeBlink*), la bouche suit la voix.
 */
export type ProfessorMood = 'idle' | 'speaking' | 'thinking';
/** Vitesse du vol à l'écran (px/s), partagée par l'enveloppe sans re-rendu. */
export interface ProfessorMotion { vx: number; vy: number; }
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
  onError: () => void;
}
export const PROFESSOR_MODEL_URL = '/media/avatar/moalim-professeur.glb';
const VIEW_WIDTH = 180, VIEW_HEIGHT = 260;
/** Le canevas déborde de la boîte de chaque côté : un bras tendu n'est jamais coupé. */
const CANVAS_MARGIN = 120, CANVAS_WIDTH = VIEW_WIDTH + 2 * CANVAS_MARGIN;
const CAMERA = { fov: 30, position: new THREE.Vector3(0, 1.36, 2.35), lookAt: new THREE.Vector3(0, 1.3, 0) };
const FINGERS = ['Index', 'Middle', 'Ring', 'Pinky'] as const;

export default function Professor3D({ mood, pointing, pointingSide, target, writing = false, motion, onHandPosition, onError }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const moodRef = useRef(mood), pointRef = useRef(pointing), sideRef = useRef(pointingSide), targetRef = useRef(target), writingRef = useRef(writing);
  const motionRef = useRef(motion);
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
    const camera = new THREE.PerspectiveCamera(CAMERA.fov, CANVAS_WIDTH / VIEW_HEIGHT, 0.05, 50);
    camera.position.copy(CAMERA.position);
    camera.lookAt(CAMERA.lookAt);
    scene.add(new THREE.HemisphereLight(0xffffff, 0x6b7280, 1.6));
    const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(-1.5, 2.8, 2.6); scene.add(key);
    const fill = new THREE.DirectionalLight(0xdbe4ff, 0.9); fill.position.set(1.8, 1.6, 2); scene.add(fill);
    const rim = new THREE.DirectionalLight(0xffffff, 0.8); rim.position.set(0, 2.4, -2.5); scene.add(rim);

    let disposed = false, frame = 0;
    let model: THREE.Object3D | null = null;
    let mixer: THREE.AnimationMixer | null = null;
    const bones = new Map<string, THREE.Bone>();
    const faces: THREE.Mesh[] = [];
    const clock = new THREE.Clock();
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let speech = 0, talk = 0, think = 0, aim = 0, lean = 0, rise = 0, scribe = 0;
    let aimSide: 'Left' | 'Right' = 'Right';
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
        if (object instanceof THREE.Bone) bones.set(object.name.replace(/^mixamorig:?/, ''), object);
        if (object instanceof THREE.Mesh) {
          object.frustumCulled = false;
          if (object.morphTargetDictionary && Object.keys(object.morphTargetDictionary).length) faces.push(object);
        }
      });
      if (!bones.has('Head') || !bones.has('RightArm') || !bones.has('LeftArm')) { disposeModel(model); model = null; onError(); return; }
      scene.add(model);
      mixer = new THREE.AnimationMixer(model);
      const idle = gltf.animations.find(clip => /idle/i.test(clip.name)) ?? gltf.animations[0];
      if (idle) mixer.clipAction(idle).play();
      container.dataset.ready = 'true';
    }, undefined, () => { if (!disposed) onError(); });

    function render() {
      if (disposed) return;
      const delta = Math.min(clock.getDelta(), 0.1);
      const time = clock.elapsedTime;
      const ease = (k: number) => 1 - Math.exp(-delta * k);
      const { weights, amplitude } = sampleAvatarAudio();
      const speaking = moodRef.current === 'speaking';
      speech += (Math.min(1, amplitude * 4) - speech) * ease(4);
      talk += ((speaking ? 1 : 0) - talk) * ease(2.5);
      think += ((moodRef.current === 'thinking' ? 1 : 0) - think) * ease(2.5);
      const pointingNow = pointRef.current && !!targetRef.current;
      if (pointingNow && aim < 0.05) aimSide = sideRef.current === 'right' ? 'Left' : 'Right';   // il lui fait face : sa gauche est à droite de l'écran
      aim += ((pointingNow ? 1 : 0) - aim) * ease(5);
      const flight = motionRef.current?.current;
      lean += (THREE.MathUtils.clamp((flight?.vx ?? 0) / 700, -1, 1) - lean) * ease(6);
      rise += (THREE.MathUtils.clamp(Math.hypot(flight?.vx ?? 0, flight?.vy ?? 0) / 700, 0, 1) - rise) * ease(6);
      scribe += ((writingRef.current ? 1 : 0) - scribe) * ease(6);

      if (mixer && model) {
        mixer.timeScale = reducedMotion.matches ? 0.3 : 1;
        mixer.update(delta);
        model.updateMatrixWorld(true);
        if (!reducedMotion.matches) {
          // Gestes d'explication : fenêtres alternées, avec des pauses, plus amples quand la voix porte.
          const beat = (period: number, offset: number) => { const p = (time + offset) % period; return p < 3.2 ? Math.sin(Math.PI * p / 3.2) ** 2 : 0; };
          const gestureR = talk * (0.55 + 0.45 * speech) * beat(6.1, 0.3);
          const gestureL = talk * (0.55 + 0.45 * speech) * beat(7.3, 3.4);
          const both = talk * 0.35;
          // Vol : le corps penche dans le sens du déplacement, les jambes traînent derrière.
          rotateWorld(bone('Hips'), Z, -lean * 0.22);
          rotateWorld(bone('Spine'), X, rise * 0.12);
          for (const leg of ['LeftUpLeg', 'RightUpLeg']) rotateWorld(bone(leg), X, -rise * 0.35);
          for (const knee of ['LeftLeg', 'RightLeg']) rotateWorld(bone(knee), X, rise * 0.5);
          rotateWorld(bone('Spine2'), Y, talk * Math.sin(time * 0.9) * 0.05);
          rotateWorld(bone('Head'), X, -talk * (0.03 + speech * 0.05) * Math.sin(time * 2.3) + think * -0.12);
          rotateWorld(bone('Head'), Z, think * 0.12 + talk * Math.sin(time * 0.7) * 0.03);
          for (const [side, g, sign] of [['Right', gestureR, -1], ['Left', gestureL, 1]] as const) {
            if (side === aimSide && aim > 0.02) continue;
            const lift = Math.min(1, both + g);
            rotateWorld(bone(`${side}Arm`), X, -lift * 0.42);                                 // bras vers l'avant
            rotateWorld(bone(`${side}Arm`), Z, sign * lift * 0.28);                           // et écarté du corps
            const elbowBone = bone(`${side}ForeArm`);
            rotateWorld(elbowBone, X, -lift * (1.45 + 0.2 * Math.sin(time * 3.1 + (sign > 0 ? 1 : 0))));   // main à hauteur de poitrine
            rotateWorld(elbowBone, Y, -sign * lift * 0.35);                                  // avant-bras ouvert vers l'extérieur
            const handBone = bone(`${side}Hand`);
            if (elbowBone && handBone) {
              elbowBone.getWorldPosition(vA); handBone.getWorldPosition(vB);
              rotateWorld(handBone, vB.sub(vA).normalize(), -sign * lift * 1.1);              // paume tournée vers le haut
            }
            rotateWorld(handBone, Z, sign * g * 0.3 * Math.sin(time * 2.2));
            for (const finger of FINGERS) curlFinger(side, finger, 0.15 + 0.1 * lift);
          }
          // Pointage réel : épaule puis coude vers la cible, index tendu, autres doigts repliés.
          const goal = targetRef.current;
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
        }
      }

      // Visage : actif seulement si le modèle exporte des formes faciales.
      if (time >= nextBlink) { blinkStarted = time; nextBlink = time + 3.1 + (Math.sin(++blinkCount * 2.39) + 1) * 1.8; }
      const blinkAge = time - blinkStarted;
      const blink = blinkAge > 0.2 ? 0 : Math.sin(Math.PI * blinkAge / 0.2);
      const jaw = Math.min(0.5, amplitude * 0.9);
      for (const mesh of faces) {
        const dict = mesh.morphTargetDictionary!, influences = mesh.morphTargetInfluences!;
        for (const [name, index] of Object.entries(dict)) {
          if (name.startsWith('viseme_')) influences[index] = weights[name] || 0;
          else if (name === 'jawOpen' || name === 'mouthOpen') influences[index] = jaw;
          else if (name === 'eyeBlinkLeft' || name === 'eyeBlinkRight' || name === 'eyesClosed') influences[index] = blink;
          else if (name === 'mouthSmile' || name === 'mouthSmileLeft' || name === 'mouthSmileRight') influences[index] = 0.15;
        }
      }
      container!.dataset.mouth = String(jaw);
      container!.dataset.aim = aim.toFixed(2);
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
      mixer?.stopAllAction();
      if (model) disposeModel(model);
      renderer.domElement.removeEventListener('webglcontextlost', lost);
      renderer.dispose();
      renderer.domElement.remove();
    };
  }, [onError, onHandPosition]);
  return <div ref={host} className="moalim-avatar__3d" role="img" aria-label="Professeur Moalim animé" />;
}
