import { useEffect, useRef, useState } from 'react';
import { Pause, Play, RefreshCcw, Rotate3D, ZoomIn } from 'lucide-react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import type {
  Mitochondrion3DPart,
  Mitochondrion3DVisualSpec,
} from './types';

interface Mitochondrion3DVisualProps {
  spec: Mitochondrion3DVisualSpec;
  transparent?: boolean;
}

type PartMaterial = THREE.MeshPhysicalMaterial;

const PARTS: Array<{ id: Mitochondrion3DPart; label: string; color: string }> = [
  { id: 'all', label: 'Vue globale', color: '#e2e8f0' },
  { id: 'outer_membrane', label: 'Membrane externe', color: '#fb7185' },
  { id: 'intermembrane_space', label: 'Espace intermembranaire', color: '#7dd3fc' },
  { id: 'inner_membrane', label: 'Membrane interne', color: '#fdba74' },
  { id: 'cristae', label: 'Crêtes', color: '#fde68a' },
  { id: 'matrix', label: 'Matrice', color: '#5eead4' },
  { id: 'mitochondrial_dna', label: 'ADN mitochondrial', color: '#c4b5fd' },
];

const FALLBACK_IMAGE = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_3d_sans_legendes.png';

function material(
  part: Exclude<Mitochondrion3DPart, 'all' | 'intermembrane_space'>,
  color: number,
  opacity: number,
  options: Partial<THREE.MeshPhysicalMaterialParameters> = {},
): PartMaterial {
  const result = new THREE.MeshPhysicalMaterial({
    color,
    emissive: color,
    emissiveIntensity: 0.08,
    metalness: 0.03,
    roughness: 0.48,
    clearcoat: 0.3,
    clearcoatRoughness: 0.35,
    transparent: opacity < 1,
    opacity,
    side: THREE.DoubleSide,
    depthWrite: opacity >= 0.9,
    ...options,
  });
  result.userData = {
    part,
    baseOpacity: opacity,
    baseEmissiveIntensity: result.emissiveIntensity,
  };
  return result;
}

function tag(mesh: THREE.Mesh, part: Exclude<Mitochondrion3DPart, 'all' | 'intermembrane_space'>) {
  mesh.userData.part = part;
  mesh.renderOrder = part === 'outer_membrane' ? 5 : part === 'inner_membrane' ? 4 : 2;
  return mesh;
}

function applyFocus(scene: THREE.Scene, focus: Mitochondrion3DPart) {
  const spaceHighlighted = focus === 'intermembrane_space';
  scene.traverse(object => {
    if (!(object instanceof THREE.Mesh)) return;
    const part = object.userData.part as Mitochondrion3DPart | undefined;
    const materials = Array.isArray(object.material) ? object.material : [object.material];
    for (const candidate of materials) {
      const value = candidate as PartMaterial;
      if (!value.userData?.part) continue;
      const baseOpacity = Number(value.userData.baseOpacity ?? 1);
      const baseEmissive = Number(value.userData.baseEmissiveIntensity ?? 0.08);
      const active = focus === 'all'
        || part === focus
        || (spaceHighlighted && (part === 'outer_membrane' || part === 'inner_membrane'));
      value.opacity = focus === 'all' ? baseOpacity : active ? Math.min(1, baseOpacity + 0.34) : baseOpacity * 0.24;
      value.emissiveIntensity = focus === 'all' ? baseEmissive : active ? 0.72 : 0.015;
      value.needsUpdate = true;
    }
  });
}

function buildMitochondrion(scene: THREE.Scene) {
  const group = new THREE.Group();
  group.name = 'Mitochondrie';
  group.rotation.set(-0.12, 0.22, -0.08);
  scene.add(group);

  const matrixGeometry = new THREE.CapsuleGeometry(1.08, 3.15, 12, 48);
  const matrix = tag(new THREE.Mesh(
    matrixGeometry,
    material('matrix', 0x2dd4bf, 0.25, { transmission: 0.05, depthWrite: false }),
  ), 'matrix');
  matrix.rotation.z = Math.PI / 2;
  group.add(matrix);

  const innerGeometry = new THREE.CapsuleGeometry(1.25, 3.3, 12, 48);
  const inner = tag(new THREE.Mesh(
    innerGeometry,
    material('inner_membrane', 0xfb923c, 0.17, { transmission: 0.1, depthWrite: false }),
  ), 'inner_membrane');
  inner.rotation.z = Math.PI / 2;
  group.add(inner);

  const outerGeometry = new THREE.CapsuleGeometry(1.42, 3.45, 12, 48);
  const outer = tag(new THREE.Mesh(
    outerGeometry,
    material('outer_membrane', 0xf43f5e, 0.28, {
      transmission: 0.08,
      clearcoat: 0.7,
      depthWrite: false,
    }),
  ), 'outer_membrane');
  outer.rotation.z = Math.PI / 2;
  group.add(outer);

  [-2.12, -1.42, -0.71, 0, 0.71, 1.42, 2.12].forEach((x, index) => {
    const width = 0.5 + (index % 2) * 0.06;
    const curve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, 0.94, -width),
      new THREE.Vector3(0, 0.35, -width * 1.28),
      new THREE.Vector3(0, -0.56, -width * 0.92),
      new THREE.Vector3(0, -0.86, 0),
      new THREE.Vector3(0, -0.56, width * 0.92),
      new THREE.Vector3(0, 0.35, width * 1.28),
      new THREE.Vector3(0, 0.94, width),
    ], false, 'catmullrom', 0.42);
    const fold = tag(new THREE.Mesh(
      new THREE.TubeGeometry(curve, 56, 0.06, 10, false),
      material('cristae', 0xfde68a, 0.94, {
        emissive: 0xfbbf24,
        emissiveIntensity: 0.2,
        roughness: 0.32,
        clearcoat: 0.55,
      }),
    ), 'cristae');
    fold.position.set(x, Math.sin(index * 1.7) * 0.04, 0);
    fold.rotation.y = (index - 3) * 0.018;
    group.add(fold);
  });

  const dna = tag(new THREE.Mesh(
    new THREE.TorusGeometry(0.25, 0.035, 10, 72),
    material('mitochondrial_dna', 0xa78bfa, 1, {
      emissive: 0x8b5cf6,
      emissiveIntensity: 0.35,
      roughness: 0.28,
    }),
  ), 'mitochondrial_dna');
  dna.position.set(1.72, -0.72, 0.78);
  dna.rotation.x = Math.PI / 2;
  dna.rotation.z = -0.35;
  group.add(dna);

  return group;
}

export default function Mitochondrion3DVisual({ spec, transparent }: Mitochondrion3DVisualProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const resetRef = useRef<() => void>(() => undefined);
  const autoRotateRef = useRef(spec.autoplay !== false);
  const [autoRotate, setAutoRotate] = useState(spec.autoplay !== false);
  const [focus, setFocus] = useState<Mitochondrion3DPart>(spec.focus || 'all');
  const [compact, setCompact] = useState(false);
  const [webGLUnavailable, setWebGLUnavailable] = useState(false);

  useEffect(() => {
    autoRotateRef.current = autoRotate;
  }, [autoRotate]);

  useEffect(() => {
    const next = spec.focus || 'all';
    setFocus(next);
  }, [spec.focus]);

  useEffect(() => {
    if (sceneRef.current) applyFocus(sceneRef.current, focus);
  }, [focus]);

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
      setWebGLUnavailable(true);
      return undefined;
    }

    const scene = new THREE.Scene();
    sceneRef.current = scene;
    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
    camera.position.set(7.4, 3.4, 7.6);

    renderer.setClearColor(0x000000, 0);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.12;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.065;
    controls.enablePan = false;
    controls.minDistance = 4.7;
    controls.maxDistance = 14;
    controls.autoRotateSpeed = 0.72;
    controls.target.set(0, 0, 0);

    scene.add(new THREE.HemisphereLight(0xdbeafe, 0x172554, 2.4));
    const keyLight = new THREE.DirectionalLight(0xffffff, 3.8);
    keyLight.position.set(4, 6, 7);
    scene.add(keyLight);
    const rimLight = new THREE.PointLight(0x38bdf8, 22, 18);
    rimLight.position.set(-5, -2, 4);
    scene.add(rimLight);
    const warmLight = new THREE.PointLight(0xf59e0b, 15, 14);
    warmLight.position.set(4, 1, -5);
    scene.add(warmLight);

    buildMitochondrion(scene);
    applyFocus(scene, focus);

    const reset = () => {
      camera.position.set(7.4, 3.4, 7.6);
      controls.target.set(0, 0, 0);
      controls.update();
    };
    resetRef.current = reset;

    const resize = () => {
      const parent = canvas.parentElement;
      if (!parent) return;
      const { width, height } = parent.getBoundingClientRect();
      if (width < 2 || height < 2) return;
      const nextCompact = height < 300 || width < 480;
      setCompact(previous => previous === nextCompact ? previous : nextCompact);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
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
    });

    const onContextLost = (event: Event) => {
      event.preventDefault();
      setWebGLUnavailable(true);
    };
    canvas.addEventListener('webglcontextlost', onContextLost);

    return () => {
      canvas.removeEventListener('webglcontextlost', onContextLost);
      observer.disconnect();
      renderer.setAnimationLoop(null);
      controls.dispose();
      const geometries = new Set<THREE.BufferGeometry>();
      const materials = new Set<THREE.Material>();
      scene.traverse(object => {
        if (!(object instanceof THREE.Mesh)) return;
        geometries.add(object.geometry);
        const values = Array.isArray(object.material) ? object.material : [object.material];
        values.forEach(value => materials.add(value));
      });
      geometries.forEach(value => value.dispose());
      materials.forEach(value => value.dispose());
      renderer.dispose();
      sceneRef.current = null;
    };
  // La géométrie est versionnée par `model`; les changements d'état sont
  // appliqués sans reconstruire le contexte WebGL.
  }, [spec.model]);

  if (webGLUnavailable) {
    return (
      <figure className="flex h-full min-h-48 w-full flex-col items-center justify-center gap-3 overflow-hidden rounded-xl bg-slate-950 p-4 text-center text-slate-200">
        <img src={FALLBACK_IMAGE} alt="Coupe d'une mitochondrie montrant les membranes, les crêtes et la matrice" className="min-h-0 max-h-64 flex-1 rounded-lg object-contain" />
        <figcaption className="text-xs text-slate-400">Le rendu 3D n’est pas disponible sur cet appareil. La coupe scientifique statique reste affichée.</figcaption>
      </figure>
    );
  }

  const description = spec.description
    || 'Modèle pédagogique en coupe d’une mitochondrie : membrane externe, espace intermembranaire, membrane interne repliée en crêtes, matrice et ADN mitochondrial circulaire.';

  return (
    <figure
      className={`relative h-full min-h-48 w-full overflow-hidden rounded-xl ${transparent
        ? 'bg-transparent'
        : 'bg-[radial-gradient(circle_at_50%_42%,rgba(14,116,144,0.2),rgba(2,6,23,0.96)_72%)]'}`}
      data-scientific-engine="three"
      data-scientific-model="mitochondrion"
    >
      <canvas
        ref={canvasRef}
        className="absolute inset-0 h-full w-full cursor-grab touch-none active:cursor-grabbing"
        role="img"
        aria-label={description}
        onDoubleClick={() => resetRef.current()}
      />

      {!compact && (
        <figcaption className="pointer-events-none absolute left-3 top-3 max-w-[58%] rounded-xl border border-white/10 bg-slate-950/65 px-3 py-2 backdrop-blur">
          <div className="text-sm font-bold text-white">{spec.title || 'Mitochondrie 3D interactive'}</div>
          <div className="mt-0.5 flex items-center gap-2 text-[10px] text-cyan-100/75">
            <Rotate3D className="h-3.5 w-3.5" /> Glisser pour tourner
            <ZoomIn className="ml-1 h-3.5 w-3.5" /> Molette ou pincement pour zoomer
          </div>
        </figcaption>
      )}

      <div className="absolute right-2 top-2 flex gap-1.5" aria-label="Commandes du modèle 3D">
        <button
          type="button"
          onClick={() => setAutoRotate(value => !value)}
          className="grid h-8 w-8 place-items-center rounded-lg border border-white/15 bg-slate-950/75 text-cyan-100 shadow-lg backdrop-blur hover:bg-cyan-500/25"
          title={autoRotate ? 'Arrêter la rotation automatique' : 'Lancer la rotation automatique'}
          aria-label={autoRotate ? 'Arrêter la rotation automatique' : 'Lancer la rotation automatique'}
        >
          {autoRotate ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
        </button>
        <button
          type="button"
          onClick={() => resetRef.current()}
          className="grid h-8 w-8 place-items-center rounded-lg border border-white/15 bg-slate-950/75 text-cyan-100 shadow-lg backdrop-blur hover:bg-cyan-500/25"
          title="Recentrer la mitochondrie"
          aria-label="Recentrer la mitochondrie"
        >
          <RefreshCcw className="h-3.5 w-3.5" />
        </button>
      </div>

      {compact ? (
        <div className="pointer-events-none absolute bottom-2 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-full border border-white/10 bg-slate-950/70 px-2.5 py-1 text-[9px] font-semibold text-cyan-100/80 backdrop-blur">
          Glisser · zoomer · double-clic pour recentrer
        </div>
      ) : spec.labels !== false && (
        <div className="absolute bottom-2 left-2 right-2 flex flex-wrap justify-center gap-1 rounded-xl border border-white/10 bg-slate-950/70 p-1.5 backdrop-blur" aria-label="Légende interactive de la mitochondrie">
          {PARTS.map(part => (
            <button
              key={part.id}
              type="button"
              onClick={() => setFocus(part.id)}
              className={`flex items-center gap-1.5 rounded-lg px-2 py-1 text-[10px] font-semibold transition ${focus === part.id
                ? 'bg-white/15 text-white ring-1 ring-cyan-300/50'
                : 'text-slate-300 hover:bg-white/10 hover:text-white'}`}
              aria-pressed={focus === part.id}
            >
              <span className="h-2 w-2 rounded-full" style={{ backgroundColor: part.color }} />
              {part.label}
            </button>
          ))}
        </div>
      )}
      <p className="sr-only">{description}</p>
    </figure>
  );
}
