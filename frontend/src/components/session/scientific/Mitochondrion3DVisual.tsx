import { useEffect, useRef, useState } from 'react';
import {
  Box,
  Image as ImageIcon,
  LoaderCircle,
  Pause,
  Play,
  RefreshCcw,
  Rotate3D,
  Tags,
  ZoomIn,
} from 'lucide-react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import type { Mitochondrion3DPart, Mitochondrion3DVisualSpec } from './types';

interface Mitochondrion3DVisualProps {
  spec: Mitochondrion3DVisualSpec;
  transparent?: boolean;
}

const MODEL_FILE = '/media/models/svt/mitochondria/mitochondria-captaainro-web.glb';
const FALLBACK_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_3d_sans_legendes.png';
const MODEL_PAGE = 'https://sketchfab.com/3d-models/mitochondria-b6726ede64d34fb5bedb02765b4d49c0';
const LICENSE_PAGE = 'https://creativecommons.org/licenses/by/4.0/';

type LabelPart = Exclude<Mitochondrion3DPart, 'all'>;

interface ModelLabel {
  id: LabelPart;
  label: string;
  color: string;
  side: 'left' | 'right';
  row: number;
  /** Coordonnées dans la scène normalisée, jamais fournies par le LLM. */
  point: readonly [number, number, number];
}

const FOCUS_LABELS: Record<LabelPart, string> = {
  outer_membrane: 'membrane externe',
  intermembrane_space: 'espace intermembranaire',
  inner_membrane: 'membrane interne',
  cristae: 'crêtes mitochondriales',
  matrix: 'matrice',
  mitochondrial_dna: 'ADN mitochondrial',
};

const MODEL_LABELS: readonly ModelLabel[] = [
  {
    id: 'outer_membrane', label: 'Membrane externe', color: '#fb7185',
    side: 'right', row: 0.35, point: [2.4, 0.15, 0.7],
  },
  {
    id: 'intermembrane_space', label: 'Espace intermembranaire', color: '#7dd3fc',
    side: 'left', row: 0.52, point: [-2.2, 0.52, 0.65],
  },
  {
    id: 'matrix', label: 'Matrice', color: '#2dd4bf',
    side: 'left', row: 0.69, point: [-0.35, -0.12, 0.72],
  },
  {
    id: 'inner_membrane', label: 'Membrane interne', color: '#fdba74',
    side: 'left', row: 0.35, point: [-1.7, 0.42, 0.75],
  },
  {
    id: 'cristae', label: 'Crêtes', color: '#fde047',
    side: 'right', row: 0.52, point: [-1.05, 0.08, 0.8],
  },
  {
    id: 'mitochondrial_dna', label: 'ADN mitochondrial', color: '#c4b5fd',
    side: 'right', row: 0.69, point: [0.1, -0.06, 0.75],
  },
];

const DEFAULT_CAMERA_POSITION = new THREE.Vector3(7.1, 4.5, 8.7);

function disposeModel(root: THREE.Object3D) {
  const textures = new Set<THREE.Texture>();
  const materials = new Set<THREE.Material>();

  root.traverse((object) => {
    if (!(object instanceof THREE.Mesh)) return;
    object.geometry?.dispose();
    const meshMaterials = Array.isArray(object.material) ? object.material : [object.material];
    meshMaterials.forEach((material) => {
      materials.add(material);
      Object.values(material).forEach((value) => {
        if (value instanceof THREE.Texture) textures.add(value);
      });
    });
  });

  textures.forEach((texture) => texture.dispose());
  materials.forEach((material) => material.dispose());
}

export default function Mitochondrion3DVisual({ spec, transparent }: Mitochondrion3DVisualProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const resetRef = useRef<() => void>(() => undefined);
  const autoRotateRef = useRef(spec.autoplay !== false);
  const labelPathRefs = useRef<Partial<Record<LabelPart, SVGPathElement | null>>>({});
  const labelDotRefs = useRef<Partial<Record<LabelPart, SVGCircleElement | null>>>({});
  const [view, setView] = useState<'model' | 'image'>('model');
  const [autoRotate, setAutoRotate] = useState(spec.autoplay !== false);
  const [labelsVisible, setLabelsVisible] = useState(spec.labels !== false);
  const [isModelMoving, setIsModelMoving] = useState(spec.autoplay !== false);
  const [modelReady, setModelReady] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [modelError, setModelError] = useState<string | null>(null);

  useEffect(() => {
    autoRotateRef.current = autoRotate;
  }, [autoRotate]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return undefined;

    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({
        canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance',
      });
    } catch {
      const errorTimer = window.setTimeout(() => {
        setModelError('Le rendu 3D n’est pas disponible sur cet appareil.');
      }, 0);
      return () => window.clearTimeout(errorTimer);
    }

    let disposed = false;
    let modelRoot: THREE.Object3D | null = null;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
    camera.position.copy(DEFAULT_CAMERA_POSITION);

    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.6));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.18;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.065;
    controls.enablePan = false;
    controls.minDistance = 5.3;
    controls.maxDistance = 18;
    controls.autoRotateSpeed = 0.72;
    controls.target.set(0, 0, 0);
    const projectedLabel = new THREE.Vector3();
    let movementEndTimer: number | null = null;

    // Les points d’ancrage sont fiables dans la vue initiale, mais pas
    // lorsque l’élève fait pivoter la caméra autour du modèle. Les légendes
    // restent donc masquées après une interaction jusqu’à ce que l’élève
    // demande explicitement la vue légendée, qui recentre la caméra.
    const hideLabelsWhileMoving = () => {
      if (disposed) return;
      setIsModelMoving(true);
      setLabelsVisible(false);
      if (movementEndTimer !== null) window.clearTimeout(movementEndTimer);
      movementEndTimer = window.setTimeout(() => {
        if (!disposed) setIsModelMoving(false);
      }, 120);
    };

    controls.addEventListener('start', hideLabelsWhileMoving);

    scene.add(new THREE.HemisphereLight(0xf8fafc, 0x172554, 2.5));
    const keyLight = new THREE.DirectionalLight(0xffffff, 4.2);
    keyLight.position.set(5, 7, 8);
    scene.add(keyLight);
    const fillLight = new THREE.DirectionalLight(0x67e8f9, 2.1);
    fillLight.position.set(-6, 1, 5);
    scene.add(fillLight);
    const rimLight = new THREE.DirectionalLight(0xfbbf24, 1.7);
    rimLight.position.set(2, -4, -6);
    scene.add(rimLight);

    const resetCamera = () => {
      camera.position.copy(DEFAULT_CAMERA_POSITION);
      controls.target.set(0, 0, 0);
      controls.update();
    };
    resetRef.current = resetCamera;

    const loader = new GLTFLoader();
    loader.setMeshoptDecoder(MeshoptDecoder);
    loader.load(
      MODEL_FILE,
      (gltf) => {
        if (disposed) {
          disposeModel(gltf.scene);
          return;
        }

        modelRoot = gltf.scene;
        const initialBounds = new THREE.Box3().setFromObject(modelRoot);
        const center = initialBounds.getCenter(new THREE.Vector3());
        const size = initialBounds.getSize(new THREE.Vector3());
        const longestSide = Math.max(size.x, size.y, size.z);
        const scale = longestSide > 0 ? 6.2 / longestSide : 1;
        modelRoot.scale.setScalar(scale);
        modelRoot.position.copy(center).multiplyScalar(-scale);
        scene.add(modelRoot);
        resetCamera();
        setLoadingProgress(100);
        setModelReady(true);
      },
      (event) => {
        if (disposed || event.total <= 0) return;
        setLoadingProgress(Math.min(99, Math.round((event.loaded / event.total) * 100)));
      },
      () => {
        if (disposed) return;
        setModelError('Le modèle 3D local n’a pas pu être chargé.');
      },
    );

    const resize = () => {
      const parent = canvas.parentElement;
      if (!parent) return;
      const { width, height } = parent.getBoundingClientRect();
      if (width < 2 || height < 2) return;
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
    };
    const observer = new ResizeObserver(resize);
    if (canvas.parentElement) observer.observe(canvas.parentElement);
    resize();

    renderer.setAnimationLoop(() => {
      controls.autoRotate = autoRotateRef.current;
      controls.update();
      renderer.render(scene, camera);

      const width = canvas.clientWidth;
      const height = canvas.clientHeight;
      if (width < 2 || height < 2) return;
      const labelInset = Math.min(148, Math.max(104, width * 0.27));

      MODEL_LABELS.forEach((label) => {
        const path = labelPathRefs.current[label.id];
        const dot = labelDotRefs.current[label.id];
        if (!path || !dot) return;

        projectedLabel.set(...label.point).project(camera);
        const visible = projectedLabel.z > -1 && projectedLabel.z < 1;
        const anchorX = (projectedLabel.x * 0.5 + 0.5) * width;
        const anchorY = (-projectedLabel.y * 0.5 + 0.5) * height;
        const labelX = label.side === 'left' ? labelInset : width - labelInset;
        const labelY = height * label.row;
        const elbowX = label.side === 'left' ? labelX + 14 : labelX - 14;

        path.setAttribute('d', `M ${labelX} ${labelY} L ${elbowX} ${labelY} L ${anchorX} ${anchorY}`);
        path.style.opacity = visible ? '1' : '0';
        dot.setAttribute('cx', String(anchorX));
        dot.setAttribute('cy', String(anchorY));
        dot.style.opacity = visible ? '1' : '0';
      });
    });

    const onContextLost = (event: Event) => {
      event.preventDefault();
      setModelError('Le contexte 3D a été interrompu. L’image de référence reste disponible.');
    };
    canvas.addEventListener('webglcontextlost', onContextLost);

    return () => {
      disposed = true;
      controls.removeEventListener('start', hideLabelsWhileMoving);
      if (movementEndTimer !== null) window.clearTimeout(movementEndTimer);
      canvas.removeEventListener('webglcontextlost', onContextLost);
      observer.disconnect();
      renderer.setAnimationLoop(null);
      controls.dispose();
      if (modelRoot) disposeModel(modelRoot);
      renderer.dispose();
      resetRef.current = () => undefined;
    };
  }, []);

  const description = spec.description
    || 'Modèle 3D réaliste en coupe d’une mitochondrie montrant la double membrane, les crêtes, la matrice et l’ADN mitochondrial.';
  const focusLabel = spec.focus && spec.focus !== 'all' ? FOCUS_LABELS[spec.focus] : undefined;
  const activeFocus = spec.focus || 'all';
  const showModel = view === 'model' && modelReady && !modelError;
  const showLabels = showModel && labelsVisible && !isModelMoving;

  const handleLegendToggle = () => {
    if (showLabels) {
      setLabelsVisible(false);
      return;
    }

    // La vue légendée doit toujours être la vue de référence : on arrête la
    // rotation automatique et on replace la caméra sur son cadrage initial.
    autoRotateRef.current = false;
    setAutoRotate(false);
    resetRef.current();
    setIsModelMoving(false);
    setLabelsVisible(true);
  };

  const handleAutoRotateToggle = () => {
    const nextAutoRotate = !autoRotate;
    autoRotateRef.current = nextAutoRotate;
    setAutoRotate(nextAutoRotate);
    if (nextAutoRotate) {
      setIsModelMoving(true);
      setLabelsVisible(false);
    }
  };

  return (
    <figure
      className={`relative h-full min-h-48 w-full overflow-hidden rounded-xl ${transparent
        ? 'bg-transparent'
        : 'bg-[radial-gradient(circle_at_50%_42%,rgba(30,41,59,0.65),rgba(2,6,23,0.98)_72%)]'}`}
      data-scientific-engine="three"
      data-scientific-model="mitochondrion"
      data-model-source="local-cc-by"
      data-labels-visible={showLabels ? 'true' : 'false'}
    >
      {(view === 'image' || (view === 'model' && Boolean(modelError))) && (
        <div className="absolute inset-0 grid place-items-center p-3">
          <img
            src={FALLBACK_IMAGE}
            alt="Coupe réaliste d’une mitochondrie montrant les membranes, les crêtes et la matrice"
            className="h-full w-full object-contain"
          />
        </div>
      )}

      <canvas
        ref={canvasRef}
        className={`absolute inset-0 h-full w-full touch-none transition-opacity duration-300 ${showModel
          ? 'cursor-grab opacity-100 active:cursor-grabbing'
          : 'pointer-events-none opacity-0'}`}
        role="img"
        aria-label={description}
        onDoubleClick={() => resetRef.current()}
      />

      {view === 'model' && !modelReady && !modelError && (
        <div className="pointer-events-none absolute inset-0 z-10 grid place-items-center bg-slate-950/25">
          <span className="flex items-center gap-2 rounded-full bg-slate-950/80 px-3 py-1.5 text-xs font-semibold text-cyan-50 backdrop-blur">
            <LoaderCircle className="h-4 w-4 animate-spin" />
            Chargement du modèle 3D local{loadingProgress > 0 ? ` · ${loadingProgress} %` : '…'}
          </span>
        </div>
      )}

      {view === 'model' && modelError && (
        <div className="pointer-events-none absolute bottom-12 left-1/2 z-20 w-max max-w-[88%] -translate-x-1/2 rounded-lg bg-rose-950/85 px-3 py-1.5 text-center text-[10px] font-semibold text-rose-100 backdrop-blur">
          {modelError}
        </div>
      )}

      {showLabels && (
        <div className="pointer-events-none absolute inset-0 z-10" role="list" aria-label="Légendes de la mitochondrie">
          <svg className="absolute inset-0 h-full w-full overflow-visible" aria-hidden="true">
            {MODEL_LABELS.map((label) => {
              const active = activeFocus === label.id;
              const muted = activeFocus !== 'all' && !active;
              return (
                <g key={label.id}>
                  <path
                    ref={(element) => { labelPathRefs.current[label.id] = element; }}
                    fill="none"
                    stroke={label.color}
                    strokeWidth={active ? 2.5 : 1.4}
                    strokeOpacity={muted ? 0.25 : 0.82}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="transition-opacity duration-150"
                  />
                  <circle
                    ref={(element) => { labelDotRefs.current[label.id] = element; }}
                    r={active ? 4.5 : 3.2}
                    fill={label.color}
                    stroke="#020617"
                    strokeWidth="1.5"
                    className={active ? 'animate-pulse' : ''}
                  />
                </g>
              );
            })}
          </svg>

          {MODEL_LABELS.map((label) => {
            const active = activeFocus === label.id;
            const muted = activeFocus !== 'all' && !active;
            return (
              <div
                key={label.id}
                role="listitem"
                data-label-part={label.id}
                className={`absolute flex max-w-36 -translate-y-1/2 items-center gap-1.5 rounded-lg border px-2 py-1 text-[9px] font-bold leading-tight shadow-lg backdrop-blur transition ${label.side === 'left' ? 'left-2' : 'right-2'} ${active
                  ? 'border-amber-200 bg-amber-950/90 text-amber-50 ring-1 ring-amber-300/60'
                  : 'border-white/15 bg-slate-950/82 text-slate-100'} ${muted ? 'opacity-45' : 'opacity-100'}`}
                style={{ top: `${label.row * 100}%` }}
              >
                <span className="h-2 w-2 shrink-0 rounded-full" style={{ backgroundColor: label.color }} />
                {label.label}
              </div>
            );
          })}
        </div>
      )}

      <figcaption className="pointer-events-none absolute left-3 top-3 z-20 max-w-[58%] rounded-xl border border-white/10 bg-slate-950/72 px-3 py-2 text-white shadow-lg backdrop-blur">
        <div className="text-sm font-bold">{spec.title || 'Mitochondrie 3D réaliste'}</div>
        {view === 'model' ? (
          <div className="mt-0.5 flex flex-wrap items-center gap-x-2 text-[10px] text-cyan-100/80">
            <span className="flex items-center gap-1"><Rotate3D className="h-3.5 w-3.5" /> Glisser pour tourner</span>
            <span className="flex items-center gap-1"><ZoomIn className="h-3.5 w-3.5" /> Molette ou pincement</span>
          </div>
        ) : (
          <div className="mt-0.5 text-[10px] text-cyan-100/80">Image réaliste de référence</div>
        )}
        {focusLabel && <div className="mt-1 text-[10px] font-semibold text-amber-200">À repérer : {focusLabel}</div>}
      </figcaption>

      <div className="absolute right-2 top-2 z-20 flex gap-1.5" aria-label="Commandes de la mitochondrie">
        <button
          type="button"
          onClick={() => setView((value) => value === 'model' ? 'image' : 'model')}
          className="flex h-8 items-center gap-1.5 rounded-lg border border-white/15 bg-slate-950/80 px-2.5 text-[10px] font-bold text-cyan-50 shadow-lg backdrop-blur hover:bg-cyan-500/30"
          title={view === 'model' ? 'Afficher l’image réaliste' : 'Afficher le modèle 3D'}
        >
          {view === 'model' ? <ImageIcon className="h-3.5 w-3.5" /> : <Box className="h-3.5 w-3.5" />}
          {view === 'model' ? 'Image' : '3D'}
        </button>
        {view === 'model' && (
          <>
            <button
              type="button"
              onClick={handleLegendToggle}
              className={`grid h-8 w-8 place-items-center rounded-lg border shadow-lg backdrop-blur ${showLabels
                ? 'border-cyan-300/45 bg-cyan-500/25 text-cyan-50'
                : 'border-white/15 bg-slate-950/80 text-slate-300 hover:bg-cyan-500/30'}`}
              title={showLabels ? 'Masquer les légendes' : 'Recentrer et afficher les légendes'}
              aria-label={showLabels ? 'Masquer les légendes' : 'Recentrer et afficher les légendes'}
              aria-pressed={showLabels}
            >
              <Tags className="h-3.5 w-3.5" />
            </button>
            <button
              type="button"
              onClick={handleAutoRotateToggle}
              className="grid h-8 w-8 place-items-center rounded-lg border border-white/15 bg-slate-950/80 text-cyan-50 shadow-lg backdrop-blur hover:bg-cyan-500/30"
              title={autoRotate ? 'Arrêter la rotation automatique' : 'Lancer la rotation automatique'}
              aria-label={autoRotate ? 'Arrêter la rotation automatique' : 'Lancer la rotation automatique'}
            >
              {autoRotate ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
            </button>
            <button
              type="button"
              onClick={() => resetRef.current()}
              className="grid h-8 w-8 place-items-center rounded-lg border border-white/15 bg-slate-950/80 text-cyan-50 shadow-lg backdrop-blur hover:bg-cyan-500/30"
              title="Recentrer la mitochondrie"
              aria-label="Recentrer la mitochondrie"
            >
              <RefreshCcw className="h-3.5 w-3.5" />
            </button>
          </>
        )}
      </div>

      {view === 'model' && (
        <div className="absolute bottom-2 left-2 z-20 rounded-lg border border-white/10 bg-slate-950/72 px-2 py-1 text-[9px] text-slate-300 backdrop-blur">
          Modèle 3D :{' '}
          <a className="font-semibold text-cyan-200 hover:underline" href={MODEL_PAGE} target="_blank" rel="noreferrer">CAPTAAINRO</a>
          {' · '}
          <a className="text-cyan-200 hover:underline" href={LICENSE_PAGE} target="_blank" rel="noreferrer">CC BY 4.0</a>
          {' · version Web optimisée'}
        </div>
      )}
      <p className="sr-only">{description}</p>
    </figure>
  );
}
