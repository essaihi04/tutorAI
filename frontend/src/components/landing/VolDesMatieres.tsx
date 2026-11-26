import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

/**
 * Le vol au-dessus des matières (26 novembre 2026, « quand l'élève scrolle, une revue en 3D des matières, comme s'il
 * vole au-dessus de la physique, des maths, des SVT — comme un rêve »). C'est la PREMIÈRE partie de la landing,
 * avant le tableau vivant.
 *
 * Une section haute dont la scène reste collée à l'écran : le défilement est la manette. La caméra avance dans un
 * ciel de poussière de craie et traverse quatre mondes, chacun peuplé du matériel et des manips de ses cours :
 *   — maths : une surface qui ondule, la tangente qui glisse, le cercle des complexes, une suite qui converge ;
 *   — physique : l'atome, la cuve à ondes, le laser et la fente (diffraction sur l'écran), le prisme (la lumière
 *     blanche s'ouvre en couleurs), le circuit RC (le condensateur se charge, la courbe u_C monte), le noyau qui
 *     émet une particule α ;
 *   — chimie : la molécule, deux béchers (rapide / lente), le dosage (burette, gouttes, BBT qui vire, pH-mètre),
 *     les tubes à essai et leurs solutions ;
 *   — SVT : la cellule, la double hélice d'ADN, puis un zoom dans le muscle jusqu'au
 *     sarcomère (muscle → faisceau → fibre → myofibrille → sarcomère qui se contracte).
 * Les couleurs sont celles du lexique visuel (docs/lexique-visuel) : un objet a partout le même dessin.
 *
 * Rien ne tourne hors de l'écran ; tout est dessiné par three.js (pas de modèle à télécharger).
 */

const MONDES = [
  { z: -50, couleur: '#facc15', nom: 'Les maths', phrase: 'Les courbes prennent vie : limites, dérivées, suites, complexes.', signes: ['f ′(x)', '∫', 'lim', 'uₙ', 'ln x', 'π', 'z = a + ib'] },
  { z: -150, couleur: '#22d3ee', nom: 'La physique', phrase: 'Le laser traverse la fente, le prisme ouvre les couleurs, le condensateur se charge, le noyau se désintègre.', signes: ['λ', 'τ = RC', 'v = λ·f', 'θ = λ/a', 'E = mc²', 'u_C', 'N = N₀e^(−λt)'] },
  { z: -300, couleur: '#fb923c', nom: 'La chimie', phrase: 'Les béchers changent de couleur, la burette goutte, le pH-mètre lit : vitesse, équilibre, dosage.', signes: ['pH', 'Qr', 'K', 'H₃O⁺', 'pKa', 'x_max', 't½'] },
  { z: -415, couleur: '#4ade80', nom: 'Les SVT', phrase: 'Tu entres dans la cellule, tu vois l\'ADN… puis tu plonges dans le muscle, jusqu\'au sarcomère.', signes: ['ADN', 'ATP', 'ARNm', 'codon', 'Ca²⁺', 'glucose'] },
] as const;

/** Le zoom dans le muscle : chaque étape est un objet plus fin, révélé quand on traverse le précédent. */
const ETAPES = [
  { z: -500, nom: 'le muscle' },
  { z: -520, nom: 'un faisceau de fibres' },
  { z: -538, nom: 'une fibre musculaire' },
  { z: -555, nom: 'une myofibrille' },
  { z: -574, nom: 'le sarcomère' },
] as const;
/**
 * La voix du vol (voix Bodi, lot Kaggle, frontend/public/media/audio/landing/vol_*.mp3) : à chaque monde, Moalim
 * nomme ce que l'élève voit. Chaque piste couvre une plage du défilement (`de` → `a`, de 0 à 1) ; la visite guidée
 * fait défiler la plage au rythme de sa piste, pour que la voix et l'image restent ensemble.
 */
const VOIX_VOL = [
  // `sans` : la durée du passage quand sa piste manque ou ne se charge pas (s)
  { fichier: 'vol_0_depart', de: 0, a: .04, sans: 2.5 },
  { fichier: 'vol_1_maths', de: .04, a: .24, sans: 11 },
  { fichier: 'vol_2_physique', de: .24, a: .5, sans: 14 },
  { fichier: 'vol_3_chimie', de: .5, a: .69, sans: 11 },
  { fichier: 'vol_4_svt', de: .69, a: .86, sans: 10 },
  { fichier: 'vol_5_muscle', de: .86, a: .985, sans: 11 },
  { fichier: 'fin_vol', de: .985, a: 1.001, sans: 4 },
] as const;
const VOIX_URL = (f: string) => `/media/audio/landing/${f}.mp3`;
/** Un mot clé de la phrase de fin : sa couleur et son tour (styles .lp-mot de la landing). */
const MOT = (c: string, n: number) => ({ ['--mot' as string]: c, ['--attente' as string]: `${.4 + n * .8}s` }) as React.CSSProperties;
const DEPART = 20, ARRIVEE = -561, DEBUT_ZOOM = -486;
/** Hauteur de la section, en hauteurs d'écran : le temps du vol. */
const ECRANS = 12;

// Couleurs du lexique visuel
const C = {
  proton: '#f472b6', neutron: '#a0a8b4', electron: '#60c8fa',
  laser: '#ff2a1a', verre: '#cfe8ff', incolore: '#70c2f8',
  hyaloplasme: '#60c896', membrane: '#facc60', noyau: '#966edc',
  mitoExterne: '#f0643e', mitoEspace: '#ffb06e', cretes: '#ffde96', matrice: '#56b4ec',
  A: '#dc2626', T: '#ca8a04', Cy: '#2563eb', G: '#16a34a', squelette: '#4f46e5',
  actine: '#f26b3a', myosine: '#3b6fd8', fibre: '#f08aa0', muscle: '#d9485f',
  cuivre: '#2c60d0', permanganate: '#8b2fc9', diiode: '#a0522d',
  bbt: ['#f6ce2a', '#40a854', '#2c60d0'],
};

const hasard = (a: number, b: number) => a + Math.random() * (b - a);
const borne = (x: number) => Math.min(1, Math.max(0, x));

/** Une toile : on y dessine, elle devient texture. */
function toile(l: number, h: number, dessin: (c: CanvasRenderingContext2D) => void) {
  const t = document.createElement('canvas');
  t.width = l; t.height = h;
  dessin(t.getContext('2d')!);
  return new THREE.CanvasTexture(t);
}

/** Un mot écrit à la craie, qui flotte (signes des matières, étiquettes des objets). */
function ecrit(texte: string, couleur: string, taille = 1, lueur = 18) {
  // la toile prend la largeur du texte : une étiquette longue n'est jamais coupée
  const police = "92px 'Patrick Hand','Caveat','Segoe Print',cursive";
  const mesure = document.createElement('canvas').getContext('2d')!;
  mesure.font = police;
  const l = Math.max(512, Math.ceil(mesure.measureText(texte).width + 60));
  const texture = toile(l, 160, c => {
    c.font = police;
    c.textAlign = 'center'; c.textBaseline = 'middle';
    c.shadowColor = couleur; c.shadowBlur = lueur; c.fillStyle = couleur;
    c.fillText(texte, l / 2, 84);
  });
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, transparent: true, depthWrite: false, opacity: .92 }));
  s.scale.set(9 * taille * l / 512, 2.8 * taille, 1);
  return s;
}

export default function VolDesMatieres() {
  const section = useRef<HTMLElement>(null);
  const hote = useRef<HTMLDivElement>(null);
  const [p, setP] = useState(0);
  const [echec, setEchec] = useState(false);

  useEffect(() => {
    const el = hote.current, sec = section.current;
    if (!el || !sec) return;
    let renderer: THREE.WebGLRenderer;
    try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' }); }
    catch { setEchec(true); return; }
    const petit = window.innerWidth < 768;
    renderer.setPixelRatio(Math.min(devicePixelRatio, petit ? 1.25 : 1.6));
    renderer.setClearColor(0, 0);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    el.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0a1410, 0.017);
    const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 260);
    scene.add(new THREE.HemisphereLight(0xe2f2ff, 0x10241c, 1.1));
    const soleil = new THREE.DirectionalLight(0xffffff, 1.6); soleil.position.set(6, 12, 10); scene.add(soleil);
    const lampe = new THREE.PointLight(0xffffff, 70, 90); scene.add(lampe);

    const jeter: { dispose(): void }[] = [];
    const garde = <T extends { dispose(): void }>(x: T) => { jeter.push(x); return x; };
    /** Les animations reçoivent le temps et la profondeur de la caméra. */
    // Chaque animation est rangée dans la zone (profondeur) de son objet : on n'anime que ce qui est près de la caméra
    // (devant elle jusqu'à 120 unités, derrière jusqu'à 20). `zone = null` : toujours animé.
    let zone: number | null = null;
    const animations: { f: (t: number, cz: number) => void; z: number | null }[] = [];
    const anime = { push: (f: (t: number, cz: number) => void) => { animations.push({ f, z: zone }); } };
    const fil = (couleur: string, opacity = .9) => garde(new THREE.LineBasicMaterial({ color: couleur, transparent: true, opacity }));
    const mat = (couleur: string, opacity = 1, lueur = .45) => garde(new THREE.MeshStandardMaterial({
      color: couleur, emissive: couleur, emissiveIntensity: lueur, roughness: .35, metalness: .05, transparent: opacity < 1, opacity,
    }));
    const verre = (opacity = .2, couleur = C.verre) => garde(new THREE.MeshStandardMaterial({
      color: couleur, transparent: true, opacity, roughness: .05, metalness: .1, side: THREE.DoubleSide, depthWrite: false,
    }));
    const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
    const gBille = garde(new THREE.SphereGeometry(1, 20, 14));
    const bille = (couleur: string, r: number, x = 0, y = 0, z = 0, m?: THREE.Material) => {
      const b = new THREE.Mesh(gBille, m ?? mat(couleur)); b.scale.setScalar(r); b.position.set(x, y, z); return b;
    };
    /** Un bâton (fil électrique, liaison, tige) entre deux points. */
    const baton = (A: THREE.Vector3, B: THREE.Vector3, r: number, m: THREE.Material, seg = 8) => {
      const l = new THREE.Mesh(garde(new THREE.CylinderGeometry(r, r, A.distanceTo(B), seg)), m);
      l.position.copy(A).add(B).multiplyScalar(.5);
      l.quaternion.setFromUnitVectors(V(0, 1, 0), B.clone().sub(A).normalize());
      return l;
    };
    /** Beaucoup d'objets identiques en un seul appel de dessin (les billes d'un noyau, les bases de l'ADN…). */
    const instances = (parent: THREE.Object3D, g: THREE.BufferGeometry, m: THREE.Material, mats: THREE.Matrix4[]) => {
      if (!mats.length) return;
      const im = new THREE.InstancedMesh(g, m, mats.length);
      mats.forEach((x, k) => im.setMatrixAt(k, x));
      im.computeBoundingSphere(); parent.add(im);
    };
    const place = (x: number, y: number, z: number, r: number) => new THREE.Matrix4().compose(V(x, y, z), new THREE.Quaternion(), V(r, r, r));
    const etiquette = (parent: THREE.Object3D, texte: string, couleur: string, x: number, y: number, z = 0, taille = .55) => {
      const s = ecrit(texte, couleur, taille, 10); s.position.set(x, y, z);
      jeter.push(s.material.map!, s.material); parent.add(s); return s;
    };
    const ligne = (pts: THREE.Vector3[], couleur: string, opacity = .9) =>
      new THREE.Line(garde(new THREE.BufferGeometry().setFromPoints(pts)), fil(couleur, opacity));
    /** Un groupe qui flotte doucement. */
    const flotte = (g: THREE.Object3D, amp = .5, vitesse = .5) => {
      const y0 = g.position.y, d = hasard(0, 6);
      anime.push(t => { g.position.y = y0 + Math.sin(t * vitesse + d) * amp; });
    };

    // ── La poussière de craie : tout le long du vol ──
    {
      const n = petit ? 1200 : 3000, pos = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) { pos[i * 3] = hasard(-70, 70); pos[i * 3 + 1] = hasard(-40, 40); pos[i * 3 + 2] = hasard(ARRIVEE - 60, DEPART + 10); }
      const g = garde(new THREE.BufferGeometry()); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      const m = garde(new THREE.PointsMaterial({ color: 0xe2e8f0, size: .3, transparent: true, opacity: .7, depthWrite: false }));
      scene.add(new THREE.Points(g, m));
    }
    // ── Les signes de chaque matière, autour du couloir de vol ──
    for (const monde of MONDES) {
      zone = monde.z;
      monde.signes.forEach((txt, k) => {
        const s = ecrit(txt, monde.couleur);
        const cote = k % 2 ? 1 : -1;
        s.position.set(cote * hasard(14, 24), hasard(-9, 10), monde.z + 30 - k * 15);
        flotte(s, .8, .6);
        jeter.push(s.material.map!, s.material);
        scene.add(s);
      });
    }

    zone = -80;
    // ════════ MATHS ════════
    {
      const g = garde(new THREE.PlaneGeometry(70, 70, 36, 36));
      const surface = new THREE.Mesh(g, garde(new THREE.MeshBasicMaterial({ color: '#facc15', wireframe: true, transparent: true, opacity: .26 })));
      surface.rotation.x = -Math.PI / 2; surface.position.set(0, -9, -62);
      const base = g.attributes.position.array.slice() as Float32Array;
      anime.push(t => {
        const a = g.attributes.position.array as Float32Array;
        for (let i = 0; i < a.length; i += 3) a[i + 2] = Math.sin(base[i] * .22 + t * .7) * Math.cos(base[i + 1] * .22) * 2.6;
        g.attributes.position.needsUpdate = true;
      });
      scene.add(surface);
      // la parabole et sa tangente qui glisse
      const pts: THREE.Vector3[] = [];
      for (let x = -9; x <= 9; x += .3) pts.push(V(x, x * x * .16 - 4, 0));
      const parabole = ligne(pts, '#facc15'); parabole.position.set(9, 1, -60); parabole.rotation.y = -.45; parabole.scale.setScalar(1.25);
      const tangente = ligne([V(-7, 0, 0), V(7, 0, 0)], '#fb923c'); parabole.add(tangente);
      const point = bille('#fb923c', .35); parabole.add(point);
      anime.push(t => { const x = Math.sin(t * .5) * 6, y = x * x * .16 - 4; tangente.position.set(x, y, 0); tangente.rotation.z = Math.atan(.32 * x); point.position.set(x, y, 0); });
      scene.add(parabole);
      // le cercle des complexes : z = e^(iθ) qui tourne
      const plan = new THREE.Group(); plan.position.set(-10, 2, -92); plan.rotation.y = .4;
      const cercle: THREE.Vector3[] = [];
      for (let a = 0; a <= Math.PI * 2 + .01; a += .08) cercle.push(V(Math.cos(a) * 5, Math.sin(a) * 5, 0));
      plan.add(ligne(cercle, '#facc15'), ligne([V(-7, 0, 0), V(7, 0, 0)], '#e2e8f0', .6), ligne([V(0, -7, 0), V(0, 7, 0)], '#e2e8f0', .6));
      const gVec = garde(new THREE.BufferGeometry().setFromPoints([V(0, 0, 0), V(5, 0, 0)]));
      plan.add(new THREE.Line(gVec, fil('#22d3ee')));
      const pz = bille('#22d3ee', .4); plan.add(pz);
      etiquette(plan, 'Re', '#e2e8f0', 7.8, -.8); etiquette(plan, 'Im', '#e2e8f0', .9, 7.4);
      anime.push(t => {
        const a = t * .8, x = Math.cos(a) * 5, y = Math.sin(a) * 5;
        const arr = gVec.attributes.position.array as Float32Array; arr[3] = x; arr[4] = y; gVec.attributes.position.needsUpdate = true;
        pz.position.set(x, y, 0);
      });
      scene.add(plan);
      // une suite qui converge vers sa limite (uₙ = 4 + 3·(−0,7)ⁿ)
      const suite = new THREE.Group(); suite.position.set(6, -3, -112); suite.rotation.y = -.35;
      suite.add(ligne([V(-1, 0, 0), V(18, 0, 0)], '#e2e8f0', .6), ligne([V(0, -1, 0), V(0, 9, 0)], '#e2e8f0', .6));
      const limite = new THREE.Line(garde(new THREE.BufferGeometry().setFromPoints([V(0, 4, 0), V(18, 4, 0)])),
        garde(new THREE.LineDashedMaterial({ color: '#4ade80', dashSize: .5, gapSize: .35 })));
      limite.computeLineDistances(); suite.add(limite);
      etiquette(suite, 'ℓ', '#4ade80', 18.8, 4.2);
      const termes: THREE.Mesh[] = [];
      for (let n = 0; n < 14; n++) { const b = bille('#facc15', .3, 1 + n * 1.2, 4 + 3 * Math.pow(-.7, n), 0); termes.push(b); suite.add(b); }
      anime.push(t => { const k = Math.floor((t * 2.5) % 18); termes.forEach((b, n) => { b.visible = n <= k; }); });
      scene.add(suite);
    }

    // ════════ PHYSIQUE ════════
    zone = -150;
    // L'atome : noyau de protons (roses) et de neutrons (gris), électrons bleu ciel
    {
      const atome = new THREE.Group(); atome.position.set(-14, 4, -150); atome.scale.setScalar(1.2);
      const pA: THREE.Matrix4[] = [], nA: THREE.Matrix4[] = [];
      for (let k = 0; k < 12; k++) {
        const d = V(hasard(-1, 1), hasard(-1, 1), hasard(-1, 1)).normalize().multiplyScalar(k ? hasard(.5, 1.1) : 0);
        (k % 2 ? nA : pA).push(place(d.x, d.y, d.z, .62));
      }
      instances(atome, gBille, mat(C.proton), pA); instances(atome, gBille, mat(C.neutron), nA);
      const gOrbite = garde(new THREE.TorusGeometry(6, .045, 8, 90));
      [0, 1, 2].forEach(k => {
        const plan = new THREE.Group(); plan.rotation.set(k * 1.05, k * .7, 0);
        plan.add(new THREE.Mesh(gOrbite, garde(new THREE.MeshBasicMaterial({ color: '#22d3ee', transparent: true, opacity: .45 }))));
        const e = bille(C.electron, .42); plan.add(e);
        anime.push(t => { const a = t * (1.4 + k * .35) + k * 2; e.position.set(Math.cos(a) * 6, Math.sin(a) * 6, 0); });
        atome.add(plan);
      });
      anime.push(t => { atome.rotation.y = t * .25; });
      scene.add(atome);
    }
    zone = -172;
    // La cuve à ondes : une pointe frappe l'eau, les rides s'éloignent
    {
      const g = garde(new THREE.CircleGeometry(15, 80, 0, Math.PI * 2));
      const pos = g.attributes.position;
      const base = pos.array.slice() as Float32Array;
      const eau = new THREE.Mesh(g, garde(new THREE.MeshStandardMaterial({ color: '#22d3ee', emissive: '#0e7490', emissiveIntensity: .5, wireframe: true, transparent: true, opacity: .35 })));
      eau.rotation.x = -Math.PI / 2; eau.position.set(4, -8, -172);
      const pointe = bille('#e2e8f0', .45, 4, -6.6, -172);
      anime.push(t => {
        const a = pos.array as Float32Array;
        for (let i = 0; i < a.length; i += 3) { const r = Math.hypot(base[i], base[i + 1]); a[i + 2] = Math.sin(r * 1.3 - t * 4) * 1.1 / (1 + r * .12); }
        pos.needsUpdate = true;
        pointe.position.y = -6.6 + Math.sin(t * 4) * .5;
      });
      scene.add(eau, pointe);
      const e = etiquette(scene, 'cuve à ondes', '#22d3ee', 4, -4.2, -172, .6); flotte(e, .2);
    }
    zone = -196;
    // Le banc de diffraction : laser → fente → écran (taches de diffraction)
    {
      const banc = new THREE.Group(); banc.position.set(12, -1.5, -196);
      banc.add(baton(V(0, -1.6, 9), V(0, -1.6, -12), .25, mat('#475569', 1, .15)));      // le rail
      const laser = new THREE.Mesh(garde(new THREE.BoxGeometry(1.6, 1.6, 4.4)), mat('#4b5563', 1, .15)); laser.position.set(0, 0, 7); banc.add(laser);
      banc.add(bille('#ff2a1a', .3, 0, 0, 4.75));
      const rayon = baton(V(0, 0, 4.8), V(0, 0, -1), .07, mat(C.laser, 1, 2)); banc.add(rayon);
      // la plaque à fente : deux volets, une ouverture fine entre eux
      const mPlaque = mat('#1f2937', 1, .1);
      [-1, 1].forEach(s => { const v = new THREE.Mesh(garde(new THREE.BoxGeometry(2.4, 4, .2)), mPlaque); v.position.set(s * 1.32, 0, -1); banc.add(v); });
      // le faisceau qui s'ouvre après la fente (horizontalement)
      const cone = new THREE.Mesh(garde(new THREE.ConeGeometry(4.2, 10, 32, 1, true)), garde(new THREE.MeshBasicMaterial({ color: C.laser, transparent: true, opacity: .16, side: THREE.DoubleSide, depthWrite: false })));
      cone.rotation.x = Math.PI / 2; cone.scale.set(1, 1, .18); cone.position.set(0, 0, -6); banc.add(cone);
      // l'écran et sa figure : tache centrale large, taches latérales deux fois plus étroites
      const figure = toile(512, 128, c => {
        c.fillStyle = '#0b0f14'; c.fillRect(0, 0, 512, 128);
        const tache = (x: number, l: number, a: number) => {
          const gr = c.createRadialGradient(x, 64, 0, x, 64, l);
          gr.addColorStop(0, `rgba(255,60,40,${a})`); gr.addColorStop(1, 'rgba(255,0,0,0)');
          c.fillStyle = gr; c.save(); c.translate(x, 64); c.scale(1, .45); c.translate(-x, -64);
          c.beginPath(); c.arc(x, 64, l, 0, Math.PI * 2); c.fill(); c.restore();
        };
        tache(256, 70, 1);
        [1, 2, 3].forEach(k => { tache(256 + k * 70 + 35 - 0, 30, .75 / k); tache(256 - k * 70 - 35, 30, .75 / k); });
      });
      jeter.push(figure);
      const ecran = new THREE.Mesh(garde(new THREE.PlaneGeometry(10, 3.4)), garde(new THREE.MeshBasicMaterial({ map: figure })));
      ecran.position.set(0, 0, -11.2); banc.add(ecran);
      const cadre = new THREE.Mesh(garde(new THREE.BoxGeometry(10.6, 4, .3)), mat('#e2e8f0', 1, .1)); cadre.position.set(0, 0, -11.45); banc.add(cadre);
      etiquette(banc, 'laser', '#e2e8f0', 0, 1.8, 7); etiquette(banc, 'fente', '#e2e8f0', 0, 2.8, -1); etiquette(banc, 'écran', '#e2e8f0', 0, 2.8, -11);
      anime.push(t => { (cone.material as THREE.MeshBasicMaterial).opacity = .13 + Math.sin(t * 3) * .03; });
      scene.add(banc);
    }
    zone = -222;
    // Le prisme : la lumière blanche s'ouvre en couleurs, le violet le plus dévié
    {
      const pr = new THREE.Group(); pr.position.set(-14, 3, -222);
      const prisme = new THREE.Mesh(garde(new THREE.CylinderGeometry(2.6, 2.6, 3.4, 3)), verre(.35));
      prisme.rotation.x = Math.PI / 2; prisme.rotation.y = Math.PI / 2; pr.add(prisme);
      const aretes = new THREE.LineSegments(garde(new THREE.EdgesGeometry(prisme.geometry)), fil('#e2e8f0', .8)); aretes.rotation.copy(prisme.rotation); pr.add(aretes);
      pr.add(baton(V(-16, 3, 0), V(-1.2, .3, 0), .1, mat('#ffffff', 1, 2)));
      const couleurs = ['#ff2a1a', '#ff8c00', '#ffe600', '#22c55e', '#3b82f6', '#8b5cf6'];
      const rayons: THREE.Mesh[] = [];
      couleurs.forEach((c, k) => {
        const a = -.18 - k * .075, A = V(1.2, -.2, 0), B = A.clone().add(V(Math.cos(a) * 15, Math.sin(a) * 15, 0));
        const r = baton(A, B, .09, mat(c, .9, 1.6)); rayons.push(r); pr.add(r);
      });
      etiquette(pr, 'prisme', '#e2e8f0', 0, 3.6); etiquette(pr, 'lumière blanche', '#e2e8f0', -10, 4.6);
      anime.push(t => { rayons.forEach((r, k) => { (r.material as THREE.MeshStandardMaterial).opacity = .75 + Math.sin(t * 2 + k) * .2; }); });
      scene.add(pr);
    }
    zone = -248;
    // Le circuit RC : générateur, résistor, condensateur ; les électrons circulent, la courbe u_C monte
    {
      const rc = new THREE.Group(); rc.position.set(13, 1, -248); rc.rotation.y = -.35;
      const mFil = mat('#e2e8f0', 1, .2);
      const coins = [V(-6, -4, 0), V(-6, 4, 0), V(6, 4, 0), V(6, -4, 0)];
      [0, 1, 2, 3].forEach(k => rc.add(baton(coins[k], coins[(k + 1) % 4], .07, mFil)));
      // générateur : coffret gris, afficheur vert « 6V », bornes rouge et noire
      const gen = new THREE.Mesh(garde(new THREE.BoxGeometry(3.2, 2.6, 1.6)), mat('#4b5563', 1, .12)); gen.position.set(-6, 0, 0); rc.add(gen);
      const affiche = toile(128, 64, c => { c.fillStyle = '#0d1a10'; c.fillRect(0, 0, 128, 64); c.fillStyle = '#7dfc8a'; c.font = 'bold 40px monospace'; c.textAlign = 'center'; c.fillText('6V', 64, 46); });
      jeter.push(affiche);
      const ecranGen = new THREE.Mesh(garde(new THREE.PlaneGeometry(2, 1)), garde(new THREE.MeshBasicMaterial({ map: affiche }))); ecranGen.position.set(-6, .35, .81); rc.add(ecranGen);
      rc.add(bille('#dc2626', .2, -6.8, -.8, .85), bille('#111827', .2, -5.2, -.8, .85));
      // résistor : corps beige, anneaux de couleur
      const res = new THREE.Mesh(garde(new THREE.CylinderGeometry(.55, .55, 3, 20)), mat('#d6bf93', 1, .15)); res.rotation.z = Math.PI / 2; res.position.set(0, 4, 0); rc.add(res);
      ['#8b4513', '#111827', '#dc2626', '#d4a017'].forEach((c, k) => { const a = new THREE.Mesh(garde(new THREE.CylinderGeometry(.58, .58, .22, 20)), mat(c, 1, .2)); a.rotation.z = Math.PI / 2; a.position.set(-.9 + k * .55, 4, 0); rc.add(a); });
      // condensateur chimique bleu debout
      const condo = new THREE.Mesh(garde(new THREE.CylinderGeometry(.9, .9, 2.6, 24)), mat('#2f6fe0', 1, .25)); condo.position.set(6, 0, 0); rc.add(condo);
      const chapeau = new THREE.Mesh(garde(new THREE.CylinderGeometry(.92, .92, .2, 24)), mat('#9aa3ad', 1, .2)); chapeau.position.set(6, 1.35, 0); rc.add(chapeau);
      etiquette(rc, 'E', '#e2e8f0', -8.4, 0); etiquette(rc, 'R', '#e2e8f0', 0, 5.6); etiquette(rc, 'C', '#e2e8f0', 7.9, 0);
      // les électrons : vite au début de la charge, puis presque plus
      const tour = coins.map((c, k) => [c, coins[(k + 1) % 4]] as const), long = 32;
      const electrons = Array.from({ length: 10 }, (_, k) => { const b = bille(C.electron, .22); rc.add(b); return { b, s: k * long / 10 }; });
      // la courbe u_C(t) = E(1 − e^(−t/τ)), tracée au-dessus
      const courbe = new THREE.Group(); courbe.position.set(-5, 7, 0);
      courbe.add(ligne([V(0, 0, 0), V(11, 0, 0)], '#e2e8f0', .7), ligne([V(0, 0, 0), V(0, 5, 0)], '#e2e8f0', .7));
      const asym = new THREE.Line(garde(new THREE.BufferGeometry().setFromPoints([V(0, 4, 0), V(11, 4, 0)])), garde(new THREE.LineDashedMaterial({ color: '#4ade80', dashSize: .35, gapSize: .25 })));
      asym.computeLineDistances(); courbe.add(asym);
      const N = 90, gC = garde(new THREE.BufferGeometry()); gC.setAttribute('position', new THREE.BufferAttribute(new Float32Array(N * 3), 3));
      courbe.add(new THREE.Line(gC, fil('#facc15')));
      etiquette(courbe, 'u_C', '#facc15', -.6, 5.5); etiquette(courbe, 't', '#e2e8f0', 11.6, -.5);
      rc.add(courbe);
      anime.push((t, ) => {
        const cycle = 7, u = (t % cycle) / cycle;                  // 0 → 1 : une charge complète
        const vitesse = Math.exp(-u * 5);
        electrons.forEach(e => {
          e.s = (e.s + vitesse * .12) % long;
          let s = e.s;
          for (const [A, B] of tour) { const l = A.distanceTo(B); if (s <= l) { e.b.position.copy(A).lerp(B, s / l); break; } s -= l; }
        });
        const a = gC.attributes.position.array as Float32Array, n = Math.floor(u * N);
        for (let i = 0; i < N; i++) { const k = Math.min(i, n), x = k / N * 11; a[i * 3] = x; a[i * 3 + 1] = 4 * (1 - Math.exp(-x / 2.2)); a[i * 3 + 2] = 0; }
        gC.attributes.position.needsUpdate = true;
        (condo.material as THREE.MeshStandardMaterial).emissiveIntensity = .2 + (1 - vitesse) * .7;
      });
      scene.add(rc);
    }
    zone = -272;
    // Le noyau radioactif : il émet une particule α (2 protons + 2 neutrons)
    {
      const nuc = new THREE.Group(); nuc.position.set(-14, 2, -272);
      const pN: THREE.Matrix4[] = [], nN: THREE.Matrix4[] = [];
      for (let k = 0; k < 34; k++) {
        const d = V(hasard(-1, 1), hasard(-1, 1), hasard(-1, 1)).normalize().multiplyScalar(Math.cbrt(Math.random()) * 2.4);
        (k % 2 ? nN : pN).push(place(d.x, d.y, d.z, .62));
      }
      instances(nuc, gBille, mat(C.proton), pN); instances(nuc, gBille, mat(C.neutron), nN);
      const alpha = new THREE.Group();
      [[.4, .4, 0, C.proton], [-.4, -.4, 0, C.proton], [.4, -.4, .3, C.neutron], [-.4, .4, -.3, C.neutron]].forEach(([x, y, z, c]) => alpha.add(bille(c as string, .5, x as number, y as number, z as number)));
      nuc.add(alpha);
      const eclair = new THREE.PointLight('#f472b6', 0, 20); nuc.add(eclair);
      const lettre = etiquette(nuc, 'α', '#f472b6', 0, 0, 0, .8);
      etiquette(nuc, 'noyau radioactif', '#e2e8f0', 0, 4.2);
      const dir = V(1, .45, .3).normalize();
      anime.push(t => {
        const u = (t % 3.2) / 3.2;
        alpha.position.copy(dir).multiplyScalar(2.6 + u * 18);
        lettre.position.copy(alpha.position).add(V(0, 1.4, 0));
        eclair.intensity = u < .12 ? (1 - u / .12) * 60 : 0;
        nuc.rotation.y = t * .2;
      });
      scene.add(nuc);
    }

    // ════════ CHIMIE ════════
    zone = -304;
    // La molécule qui tourne
    {
      const mol = new THREE.Group(); mol.position.set(13, 3, -304); mol.scale.setScalar(1.05);
      const atomes: [number, number, number, string, number][] = [[0, 0, 0, '#fb923c', 1.5], [3.4, 1.8, 0, '#ef4444', 1.15], [-3.4, 1.8, 0, '#ef4444', 1.15], [0, -3.6, 0, '#e2e8f0', .85], [5.6, -.4, 1.5, '#e2e8f0', .7], [-5.6, -.4, -1.5, '#e2e8f0', .7]];
      const mLiaison = garde(new THREE.MeshStandardMaterial({ color: '#e2e8f0', transparent: true, opacity: .6 }));
      atomes.forEach(([x, y, z, c, r]) => mol.add(bille(c, r, x, y, z)));
      [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5]].forEach(([a, b]) => mol.add(baton(V(atomes[a][0], atomes[a][1], atomes[a][2]), V(atomes[b][0], atomes[b][1], atomes[b][2]), .16, mLiaison)));
      anime.push(t => { mol.rotation.set(Math.sin(t * .3) * .4, t * .45, 0); });
      scene.add(mol);
    }
    /** Un bécher : verre ouvert, liquide dedans. Rend le matériau du liquide pour le faire changer. */
    const becher = (parent: THREE.Object3D, x: number, y: number, z: number, r: number, h: number, couleur: string, niveau = .6) => {
      const v = new THREE.Mesh(garde(new THREE.CylinderGeometry(r, r * .96, h, 32, 1, true)), verre(.22)); v.position.set(x, y, z); parent.add(v);
      const fond = new THREE.Mesh(garde(new THREE.CircleGeometry(r * .96, 32)), verre(.3)); fond.rotation.x = -Math.PI / 2; fond.position.set(x, y - h / 2, z); parent.add(fond);
      const bord = new THREE.Mesh(garde(new THREE.TorusGeometry(r, .06, 8, 40)), mat('#e2e8f0', .7, .3)); bord.rotation.x = Math.PI / 2; bord.position.set(x, y + h / 2, z); parent.add(bord);
      const m = garde(new THREE.MeshStandardMaterial({ color: couleur, emissive: couleur, emissiveIntensity: .35, transparent: true, opacity: .75, roughness: .2 }));
      const liq = new THREE.Mesh(garde(new THREE.CylinderGeometry(r * .92, r * .9, h * niveau, 32)), m); liq.position.set(x, y - h / 2 + h * niveau / 2 + .02, z); parent.add(liq);
      return m;
    };
    zone = -322;
    // Deux béchers, le même violet : l'un se décolore d'un coup (rapide), l'autre peu à peu (lente)
    {
      const g = new THREE.Group(); g.position.set(-14, -3, -322); g.rotation.y = .45;
      const violet = new THREE.Color(C.permanganate), incolore = new THREE.Color(C.incolore);
      const rapide = becher(g, -3.2, 0, 0, 2, 4.4, C.permanganate);
      const lente = becher(g, 3.2, 0, 0, 2, 4.4, C.permanganate);
      etiquette(g, 'rapide', '#facc15', -3.2, 3.6); etiquette(g, 'lente', '#facc15', 3.2, 3.6);
      // le chronomètre entre les deux
      const chrono = new THREE.Group(); chrono.position.set(0, 4.6, 0);
      chrono.add(new THREE.Mesh(garde(new THREE.TorusGeometry(1, .1, 8, 40)), mat('#e2e8f0', 1, .3)));
      const aiguille = baton(V(0, 0, 0), V(0, .85, 0), .05, mat('#f472b6', 1, .8)); chrono.add(aiguille);
      g.add(chrono);
      anime.push(t => {
        const u = (t % 9) / 9;
        rapide.color.copy(violet).lerp(incolore, borne((u - .08) / .04)); rapide.emissive.copy(rapide.color);
        lente.color.copy(violet).lerp(incolore, borne((u - .08) / .8)); lente.emissive.copy(lente.color);
        rapide.opacity = lente.opacity = .75;
        aiguille.rotation.z = -u * Math.PI * 2;
      });
      scene.add(g);
    }
    zone = -346;
    // Le dosage : potence, burette qui goutte, erlenmeyer au BBT qui vire, pH-mètre
    {
      const d = new THREE.Group(); d.position.set(13, -3, -346); d.rotation.y = -.35;
      const mMetal = mat('#9aa3ad', 1, .15);
      const socle = new THREE.Mesh(garde(new THREE.BoxGeometry(7, .4, 4)), mat('#374151', 1, .1)); socle.position.set(0, -4.2, 0); d.add(socle);
      d.add(baton(V(-2.8, -4, 0), V(-2.8, 9, 0), .14, mMetal), baton(V(-2.8, 7, 0), V(0, 7, 0), .1, mMetal));
      // burette : tube gradué, robinet, solution titrante incolore qui baisse
      const tube = new THREE.Mesh(garde(new THREE.CylinderGeometry(.32, .32, 8, 16, 1, true)), verre(.3)); tube.position.set(0, 5, 0); d.add(tube);
      const mTitrante = garde(new THREE.MeshStandardMaterial({ color: C.incolore, emissive: C.incolore, emissiveIntensity: .3, transparent: true, opacity: .55 }));
      const titrante = new THREE.Mesh(garde(new THREE.CylinderGeometry(.27, .27, 1, 16)), mTitrante); d.add(titrante);
      for (let k = 0; k < 9; k++) d.add(baton(V(.33, 1.6 + k * .8, 0), V(.55, 1.6 + k * .8, 0), .02, mat('#e2e8f0', .8, .3)));
      d.add(baton(V(0, .9, 0), V(0, .2, 0), .06, verre(.5)), baton(V(-.4, .8, 0), V(.4, .8, 0), .08, mat('#1f2937', 1, .1)));
      // erlenmeyer (verre tourné) et sa solution au BBT
      const profil = [V(0, -4, 0), V(2.2, -4, 0), V(2.3, -3.8, 0), V(.7, -.8, 0), V(.6, .2, 0), V(.7, .3, 0)].map(v => new THREE.Vector2(v.x, v.y));
      d.add(new THREE.Mesh(garde(new THREE.LatheGeometry(profil, 36)), verre(.24)));
      const mBBT = garde(new THREE.MeshStandardMaterial({ color: C.bbt[0], emissive: C.bbt[0], emissiveIntensity: .4, transparent: true, opacity: .82 }));
      const solution = new THREE.Mesh(garde(new THREE.LatheGeometry([V(0, -3.95, 0), V(2.15, -3.95, 0), V(2.2, -3.8, 0), V(1.35, -2, 0), V(0, -2, 0)].map(v => new THREE.Vector2(v.x, v.y)), 36)), mBBT);
      d.add(solution);
      const goutte = bille(C.incolore, .14, 0, 0, 0, mTitrante); d.add(goutte);
      // pH-mètre : boîtier gris, écran vert, sonde dans l'erlenmeyer
      const boite = new THREE.Mesh(garde(new THREE.BoxGeometry(3, 2, 1)), mat('#8d959c', 1, .12)); boite.position.set(4.6, -3, 0); d.add(boite);
      const ecranT = document.createElement('canvas'); ecranT.width = 160; ecranT.height = 72;
      const ctx = ecranT.getContext('2d')!;
      const texPH = garde(new THREE.CanvasTexture(ecranT));
      const ecranPH = new THREE.Mesh(garde(new THREE.PlaneGeometry(2.2, 1)), garde(new THREE.MeshBasicMaterial({ map: texPH }))); ecranPH.position.set(4.6, -2.8, .51); d.add(ecranPH);
      d.add(baton(V(1, -2.6, 0), V(1, .6, 0), .12, mat('#1f2937', 1, .1)), bille('#cfe8ff', .22, 1, -2.7, 0, verre(.6)));
      d.add(baton(V(1, .6, 0), V(3.4, -2.2, 0), .04, mat('#111827', 1, .05)));
      etiquette(d, 'burette', '#e2e8f0', -1.6, 9.6); etiquette(d, 'pH-mètre', '#e2e8f0', 4.6, -1.2); etiquette(d, 'BBT', '#e2e8f0', -2.6, -1.4);
      let affiche = '';
      const jaune = new THREE.Color(C.bbt[0]), vert = new THREE.Color(C.bbt[1]), bleu = new THREE.Color(C.bbt[2]);
      anime.push(t => {
        const u = (t % 12) / 12;                                    // un dosage complet
        const niveau = 7.4 * (1 - u * .7);
        titrante.scale.y = niveau; titrante.position.set(0, 1.2 + niveau / 2, 0);
        const chute = (t * 1.6) % 1; goutte.position.set(0, .1 - chute * 2.1, 0); goutte.visible = u < .96;
        // pH : sigmoïde autour de l'équivalence (u = 0,6)
        const ph = 2.9 + 8.3 / (1 + Math.exp(-(u - .6) * 28));
        const c = ph < 6 ? jaune.clone() : ph < 7.6 ? jaune.clone().lerp(vert, borne((ph - 6) / 1)) : vert.clone().lerp(bleu, borne((ph - 7.6) / 1.2));
        mBBT.color.copy(c); mBBT.emissive.copy(c);
        const texte = ph.toFixed(1).replace('.', ',');
        if (texte !== affiche) {
          affiche = texte;
          ctx.fillStyle = '#9fe08a'; ctx.fillRect(0, 0, 160, 72);
          ctx.fillStyle = '#0d2a0d'; ctx.font = 'bold 44px monospace'; ctx.textAlign = 'center'; ctx.fillText(texte, 80, 52);
          texPH.needsUpdate = true;
        }
      });
      scene.add(d);
    }
    zone = -360;
    // Les tubes à essai et leurs solutions (Cu²⁺ bleu, MnO₄⁻ violet, I₂ brun, BBT vert), des bulles qui montent
    {
      const r = new THREE.Group(); r.position.set(-13, -3, -374); r.rotation.y = .25;
      const support = new THREE.Mesh(garde(new THREE.BoxGeometry(10, .5, 2.2)), mat('#8b5a2b', 1, .12)); support.position.set(0, 1, 0); r.add(support);
      const gTube = garde(new THREE.CylinderGeometry(.55, .55, 5, 18, 1, true)), gFond = garde(new THREE.SphereGeometry(.55, 18, 10, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2));
      const sols = [[C.cuivre, 'Cu²⁺'], [C.permanganate, 'MnO₄⁻'], [C.diiode, 'I₂'], [C.bbt[1], 'BBT']] as const;
      sols.forEach(([c, nom], k) => {
        const x = -3.6 + k * 2.4;
        const t = new THREE.Mesh(gTube, verre(.25)); t.position.set(x, 1.5, 0); r.add(t);
        const f = new THREE.Mesh(gFond, verre(.25)); f.position.set(x, -1, 0); r.add(f);
        const liq = new THREE.Mesh(garde(new THREE.CylinderGeometry(.5, .5, 3, 18)), mat(c, .82, .5)); liq.position.set(x, .5, 0); r.add(liq);
        r.add(bille(c, .5, x, -1, 0, liq.material as THREE.Material));
        etiquette(r, nom, '#e2e8f0', x, 5, 0, .5);
      });
      scene.add(r);
      const gB = garde(new THREE.SphereGeometry(.5, 12, 8)), mB = garde(new THREE.MeshBasicMaterial({ color: '#fb923c', transparent: true, opacity: .18 }));
      for (let k = 0; k < (petit ? 10 : 20); k++) {
        const b = new THREE.Mesh(gB, mB); const x = (Math.random() < .5 ? -1 : 1) * hasard(9, 24), z = hasard(-390, -290), v = hasard(.8, 2), d = hasard(0, 30);
        b.scale.setScalar(hasard(.3, 1.1));
        b.position.set(x, ((v * 7 + d) % 30) - 15, z);   // posée dès le départ (animée seulement quand on approche)
        anime.push(t => { b.position.set(x + Math.sin(t + d) * .6, ((t * v + d) % 30) - 15, z); });
        scene.add(b);
      }
    }

    // ════════ SVT ════════
    zone = -424;
    // La cellule : membrane dorée, hyaloplasme vert d'eau, noyau violet et nucléole, mitochondries
    {
      const cel = new THREE.Group(); cel.position.set(-15, 2, -424); cel.scale.set(1.25, 1, 1.1);
      cel.add(new THREE.Mesh(garde(new THREE.SphereGeometry(6.4, 48, 32)), garde(new THREE.MeshStandardMaterial({ color: C.membrane, emissive: C.membrane, emissiveIntensity: .25, transparent: true, opacity: .2, side: THREE.DoubleSide, depthWrite: false, roughness: .2 }))));
      cel.add(new THREE.Mesh(garde(new THREE.SphereGeometry(6.4, 28, 18)), garde(new THREE.MeshBasicMaterial({ color: C.membrane, wireframe: true, transparent: true, opacity: .18 }))));
      cel.add(new THREE.Mesh(garde(new THREE.SphereGeometry(6.1, 40, 28)), garde(new THREE.MeshStandardMaterial({ color: C.hyaloplasme, transparent: true, opacity: .14, depthWrite: false }))));
      const noyau = bille(C.noyau, 2.1, 1, .5, 0, mat(C.noyau, .9, .35)); cel.add(noyau);
      cel.add(bille('#4c2d8a', .7, 1.6, 1, .8));
      const gMito = garde(new THREE.CapsuleGeometry(.45, 1.5, 6, 14)), mMito = mat(C.mitoExterne, 1, .45);
      [[-3.2, 1.5, 1.5, .4], [-2.4, -2.6, -1, 1.2], [3.4, -2.4, 1.2, 2], [-.6, 3.6, -1.6, .8], [3.6, 2.4, -1.6, 2.6]].forEach(([x, y, z, a]) => {
        const m = new THREE.Mesh(gMito, mMito); m.position.set(x, y, z); m.rotation.set(a, a * .7, a * 1.3); cel.add(m);
      });
      instances(cel, gBille, mat('#e2e8f0'), Array.from({ length: 60 }, () => { const d = V(hasard(-1, 1), hasard(-1, 1), hasard(-1, 1)).normalize().multiplyScalar(hasard(3, 5.6)); return place(d.x, d.y, d.z, .09); }));
      etiquette(cel, 'cellule', '#4ade80', 0, 8.2, 0, .7); etiquette(cel, 'noyau', '#e2e8f0', 1, 3.4, 1.5); etiquette(cel, 'mitochondrie', '#fb923c', -3.4, -4.2, 1, .5);
      anime.push(t => { cel.rotation.y = t * .18; });
      flotte(cel, .6, .35);
      scene.add(cel);
    }
    zone = -464;
    // La molécule d'ADN : deux brins (squelette indigo) enroulés en double hélice, avec grand et petit sillon ;
    // les bases se font face au milieu : A (rouge) – T (jaune) par 2 liaisons hydrogène, C (bleu) – G (vert) par 3.
    {
      const adn = new THREE.Group(); adn.position.set(-12, 1, -464); adn.rotation.z = .4; adn.scale.setScalar(.85);
      const R = 3.2, PAS = 1.05, N = 36, TOUR = .6;          // rayon, montée par paire, nombre de paires, rotation par paire
      const DECALAGE = 2.3;                                    // les deux brins ne sont pas opposés : d'où les deux sillons
      const brin = (phase: number) => new THREE.CatmullRomCurve3(Array.from({ length: N * 2 + 1 }, (_, i) => {
        const k = i / 2, a = k * TOUR + phase; return V(Math.cos(a) * R, (k - N / 2) * PAS, Math.sin(a) * R);
      }));
      const mSq = garde(new THREE.MeshStandardMaterial({ color: C.squelette, emissive: C.squelette, emissiveIntensity: .45, roughness: .3, metalness: .15 }));
      adn.add(new THREE.Mesh(garde(new THREE.TubeGeometry(brin(0), 260, .34, 12)), mSq));
      adn.add(new THREE.Mesh(garde(new THREE.TubeGeometry(brin(DECALAGE), 260, .34, 12)), mSq));
      const gPhos = garde(new THREE.SphereGeometry(.42, 14, 10)), mPhos = mat('#818cf8', 1, .5);
      const gBase = garde(new THREE.BoxGeometry(.7, .26, 1)), mBases: Record<string, THREE.Material> = {};
      const mBase = (c: string) => (mBases[c] ??= mat(c, 1, .55));
      const mH = garde(new THREE.MeshBasicMaterial({ color: '#e2e8f0', transparent: true, opacity: .85 }));
      const gH = garde(new THREE.CylinderGeometry(.035, .035, 1, 6));
      const phos: THREE.Matrix4[] = [], liens: THREE.Matrix4[] = [], bases: Record<string, THREE.Matrix4[]> = {};
      const paires: [string, string, number][] = [[C.A, C.T, 2], [C.G, C.Cy, 3], [C.T, C.A, 2], [C.Cy, C.G, 3], [C.A, C.T, 2], [C.Cy, C.G, 3]];
      for (let k = 0; k < N; k++) {
        const y = (k - N / 2) * PAS, a1 = k * TOUR, a2 = a1 + DECALAGE;
        const P1 = V(Math.cos(a1) * R, y, Math.sin(a1) * R), P2 = V(Math.cos(a2) * R, y, Math.sin(a2) * R);
        phos.push(new THREE.Matrix4().makeTranslation(P1.x, P1.y, P1.z), new THREE.Matrix4().makeTranslation(P2.x, P2.y, P2.z));
        const [c1, c2, liaisons] = paires[(k * 5 + (k >> 2)) % paires.length];
        const dir = P2.clone().sub(P1), long = dir.length(), u = dir.clone().normalize();
        const q = new THREE.Quaternion().setFromUnitVectors(V(1, 0, 0), u);
        const ecart = .5;                                         // l'espace des liaisons hydrogène au milieu
        const l = (long - ecart) / 2;
        [[c1, P1, 1], [c2, P2, -1]].forEach(([c, P, sg]) => {
          const pos = (P as THREE.Vector3).clone().addScaledVector(u, (sg as number) * l / 2);
          (bases[c as string] ??= []).push(new THREE.Matrix4().compose(pos, q, V(l / .7, 1, 1)));
        });
        const centre = P1.clone().add(P2).multiplyScalar(.5);
        for (let h = 0; h < liaisons; h++) {
          const off = (h - (liaisons - 1) / 2) * .28;
          const pos = centre.clone().addScaledVector(V(0, 0, 1).applyQuaternion(q), off);
          liens.push(new THREE.Matrix4().compose(pos, new THREE.Quaternion().setFromUnitVectors(V(0, 1, 0), u), V(1, ecart, 1)));
        }
      }
      instances(adn, gPhos, mPhos, phos); instances(adn, gH, mH, liens);
      Object.entries(bases).forEach(([c, m]) => instances(adn, gBase, mBase(c), m));
      etiquette(adn, 'ADN : la double hélice', '#4ade80', 0, N / 2 * PAS + 2.6, 0, .85);
      etiquette(adn, 'A = T : 2 liaisons H', '#facc15', 6.8, 3, 0, .5);
      etiquette(adn, 'C ≡ G : 3 liaisons H', '#facc15', 6.8, 1.4, 0, .5);
      etiquette(adn, 'squelette', '#a5b4fc', -6.2, -6, 0, .5);
      anime.push(t => { adn.rotation.y = t * .3; });
      scene.add(adn);
    }

    // ── Le zoom dans le muscle : chaque objet s'efface quand la caméra le traverse ──
    /** Fait disparaître des matériaux quand la caméra arrive à `z` (et les remet en partant). */
    const fondu = (mats: THREE.Material[], z: number, sprites: THREE.Sprite[] = []) => {
      const base = mats.map(m => m.opacity);
      mats.forEach(m => { m.transparent = true; });
      anime.push((_, cz) => {
        const o = borne((cz - z - 2.5) / 9);
        mats.forEach((m, k) => { m.opacity = base[k] * o; m.depthWrite = o > .97; });
        sprites.forEach(s => { s.material.opacity = .92 * o; });
      });
    };
    /** Les stries d'une fibre : bandes sombres (A) et claires (I) coupées d'une strie Z. */
    const stries = (repet: number, rose: string) => {
      const tex = toile(16, 128, c => {
        c.fillStyle = rose; c.fillRect(0, 0, 16, 128);
        c.fillStyle = 'rgba(80,10,30,.55)'; c.fillRect(0, 28, 16, 72);       // bande sombre A
        c.fillStyle = 'rgba(255,255,255,.35)'; c.fillRect(0, 60, 16, 8);     // zone H
        c.fillStyle = 'rgba(40,0,10,.8)'; c.fillRect(0, 0, 16, 4); c.fillRect(0, 124, 16, 4);   // stries Z
      });
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(1, repet);
      jeter.push(tex);
      return tex;
    };
    zone = -500;
    // le muscle : un fuseau rouge-rosé, deux tendons blancs
    {
      const g = new THREE.Group(); g.position.set(0, 0, ETAPES[0].z);
      const profil: THREE.Vector2[] = [];
      for (let i = 0; i <= 24; i++) { const y = -12 + i; profil.push(new THREE.Vector2(.4 + 4.6 * Math.pow(Math.cos(Math.PI * y / 26), 1.4), y)); }
      const m1 = garde(new THREE.MeshStandardMaterial({ color: C.muscle, emissive: '#7a1020', emissiveIntensity: .4, roughness: .55, map: stries(1, '#ffffff') }));
      (m1.map as THREE.Texture).repeat.set(12, 1);
      const fuseau = new THREE.Mesh(garde(new THREE.LatheGeometry(profil, 48)), m1); fuseau.rotation.z = Math.PI / 2; g.add(fuseau);
      const m2 = mat('#f1f5f9', 1, .2);
      g.add(baton(V(-12, 0, 0), V(-17, 0, 0), .45, m2), baton(V(12, 0, 0), V(17, 0, 0), .45, m2));
      fondu([m1, m2], ETAPES[0].z);
      anime.push(t => { fuseau.scale.set(1 + Math.sin(t * 1.4) * .04, 1 - Math.sin(t * 1.4) * .03, 1 + Math.sin(t * 1.4) * .04); });
      scene.add(g);
    }
    zone = -520;
    // un faisceau : des fibres serrées dans leur gaine
    {
      const g = new THREE.Group(); g.position.set(0, 0, ETAPES[1].z);
      const mF = garde(new THREE.MeshStandardMaterial({ color: C.fibre, emissive: '#7a1030', emissiveIntensity: .35, roughness: .5, map: stries(14, '#ffffff') }));
      const gF = garde(new THREE.CylinderGeometry(.82, .82, 30, 18));
      const positions: [number, number][] = [[0, 0]];
      for (let k = 0; k < 6; k++) positions.push([Math.cos(k * Math.PI / 3) * 1.75, Math.sin(k * Math.PI / 3) * 1.75]);
      for (let k = 0; k < 12; k++) positions.push([Math.cos(k * Math.PI / 6 + .26) * 3.4, Math.sin(k * Math.PI / 6 + .26) * 3.4]);
      positions.forEach(([y, z]) => { const f = new THREE.Mesh(gF, mF); f.rotation.z = Math.PI / 2; f.position.set(0, y, z); g.add(f); });
      const mG = garde(new THREE.MeshStandardMaterial({ color: '#fbcfe8', transparent: true, opacity: .16, side: THREE.DoubleSide, depthWrite: false }));
      const gaine = new THREE.Mesh(garde(new THREE.CylinderGeometry(4.5, 4.5, 30, 32, 1, true)), mG); gaine.rotation.z = Math.PI / 2; g.add(gaine);
      fondu([mF, mG], ETAPES[1].z);
      scene.add(g);
    }
    zone = -538;
    // une fibre : un cylindre strié, ses noyaux en bordure
    {
      const g = new THREE.Group(); g.position.set(0, 0, ETAPES[2].z);
      const mF = garde(new THREE.MeshStandardMaterial({ color: C.fibre, emissive: '#7a1030', emissiveIntensity: .35, roughness: .45, map: stries(10, '#ffffff') }));
      const fibre = new THREE.Mesh(garde(new THREE.CylinderGeometry(4, 4, 32, 40)), mF); fibre.rotation.z = Math.PI / 2; g.add(fibre);
      const mN = mat(C.noyau, 1, .4);
      [[-8, 3.9, .8], [-1, -3.3, 2.3], [6, 2.6, -3]].forEach(([x, y, z]) => { const n = bille(C.noyau, 1, x, y, z, mN); n.scale.set(1.6, .45, .7); g.add(n); });
      fondu([mF, mN], ETAPES[2].z);
      scene.add(g);
    }
    zone = -555;
    // une myofibrille : plus fine, les bandes claires et sombres bien visibles
    {
      const g = new THREE.Group(); g.position.set(0, 0, ETAPES[3].z);
      const mF = garde(new THREE.MeshStandardMaterial({ color: '#f9a8c0', emissive: '#7a1030', emissiveIntensity: .3, roughness: .4, map: stries(4, '#ffffff') }));
      const myo = new THREE.Mesh(garde(new THREE.CylinderGeometry(3, 3, 34, 40)), mF); myo.rotation.z = Math.PI / 2; g.add(myo);
      const z1 = etiquette(g, 'strie Z', '#e2e8f0', -4.25, -4.4, 1, .5);
      fondu([mF], ETAPES[3].z, [z1]);
      scene.add(g);
    }
    zone = -574;
    // le sarcomère : deux stries Z, l'actine (perles rouge-orangé) qui glisse entre la myosine (bleue, à têtes)
    {
      const g = new THREE.Group(); g.position.set(0, 0, ETAPES[4].z); g.rotation.y = -.25; g.rotation.x = .12;
      const mZ = garde(new THREE.MeshStandardMaterial({ color: '#e2e8f0', emissive: '#e2e8f0', emissiveIntensity: .35, transparent: true, opacity: .55, side: THREE.DoubleSide }));
      const gZ = garde(new THREE.BoxGeometry(.25, 9, 9));
      const Z = [new THREE.Mesh(gZ, mZ), new THREE.Mesh(gZ, mZ)]; g.add(...Z);
      const mMyo = mat(C.myosine, 1, .45);
      const gEpais = garde(new THREE.CylinderGeometry(.26, .26, 7, 12));
      const grilleEpais: [number, number][] = [];
      for (const y of [-2.2, 0, 2.2]) for (const z of [-2.2, 0, 2.2]) grilleEpais.push([y, z]);
      grilleEpais.forEach(([y, z]) => { const f = new THREE.Mesh(gEpais, mMyo); f.rotation.z = Math.PI / 2; f.position.set(0, y, z); g.add(f); });
      // les têtes de myosine (instanciées), sauf dans la zone nue du milieu
      const tetes: THREE.Matrix4[] = [];
      const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), s1 = V(1, 1, 1);
      grilleEpais.forEach(([y, z]) => {
        for (let x = -3.3; x <= 3.31; x += .5) {
          if (Math.abs(x) < .8) continue;
          const a = (x * 5) % (Math.PI * 2);
          const dir = V(0, Math.cos(a), Math.sin(a));
          tetes.push(m4.clone().compose(V(x, y + dir.y * .42, z + dir.z * .42), q.setFromUnitVectors(V(0, 1, 0), dir.add(V(Math.sign(x) * -.6, 0, 0)).normalize()), s1));
        }
      });
      const instTetes = new THREE.InstancedMesh(garde(new THREE.ConeGeometry(.16, .5, 8)), mMyo, tetes.length);
      tetes.forEach((m, k) => instTetes.setMatrixAt(k, m)); g.add(instTetes);
      // l'actine : 16 filaments par côté, 14 perles chacun ; ils partent des stries Z vers le milieu
      const grilleFin: [number, number][] = [];
      for (const y of [-3.3, -1.1, 1.1, 3.3]) for (const z of [-3.3, -1.1, 1.1, 3.3]) grilleFin.push([y, z]);
      const PERLES = 14, mAct = mat(C.actine, 1, .45);
      const instAct = new THREE.InstancedMesh(garde(new THREE.SphereGeometry(.2, 10, 8)), mAct, grilleFin.length * 2 * PERLES);
      g.add(instAct);
      const lZ = etiquette(g, 'strie Z', '#e2e8f0', 0, 5.4, 0, .55);
      const lAct = etiquette(g, 'actine', C.actine, 0, -5.2, 3.3, .55);
      etiquette(g, 'myosine', '#7aa6f0', 0, 3.4, 3, .55);
      const mPos = new THREE.Matrix4(), pos = V(0, 0, 0), sc = V(1, 1, 1), qq = new THREE.Quaternion();
      anime.push(t => {
        const c = (Math.sin(t * 1.3) + 1) / 2;                   // 0 : relâché, 1 : contracté
        const demi = 6.6 - c * 1.8;                              // la demi-longueur du sarcomère
        Z[0].position.x = -demi; Z[1].position.x = demi;
        lZ.position.x = -demi; lAct.position.x = -demi + 2.2;
        let k = 0;
        for (const cote of [-1, 1]) for (const [y, z] of grilleFin) for (let i = 0; i < PERLES; i++) {
          const x = cote * (demi - .2 - i * .36);
          pos.set(x, y + Math.sin(i * 1.7) * .1, z + Math.cos(i * 1.7) * .1);
          instAct.setMatrixAt(k++, mPos.compose(pos, qq, sc));
        }
        instAct.instanceMatrix.needsUpdate = true;
      });
      scene.add(g);
    }

    zone = null;
    // ── Tout préparer avant le départ : shaders compilés et textures envoyées au GPU pendant l'écran d'accueil,
    // sinon chaque objet qui apparaît pour la première fois fige le vol un instant (à-coups des premières secondes) ──
    const preparer = () => {
      scene.traverse(o => {
        const m = (o as THREE.Mesh).material as THREE.Material | THREE.Material[] | undefined;
        (Array.isArray(m) ? m : m ? [m] : []).forEach(x => { const map = (x as THREE.MeshBasicMaterial).map; if (map) renderer.initTexture(map); });
      });
      renderer.compileAsync(scene, camera).catch(() => renderer.compile(scene, camera));
    };
    const idle = (window as Window & { requestIdleCallback?: (f: () => void) => number }).requestIdleCallback;
    if (idle) idle(preparer); else setTimeout(preparer, 300);
    // Mesure (développement seulement) : temps des animations et du rendu par image, par tranche de profondeur
    const mesures: Record<string, { n: number; anim: number; rendu: number; appels: number }> = {};
    const mesurer = (anim: number, rendu: number, z: number) => {
      const k = String(Math.round(z / 20) * 20), m = (mesures[k] ??= { n: 0, anim: 0, rendu: 0, appels: 0 });
      m.n++; m.anim += anim; m.rendu += rendu; m.appels = Math.max(m.appels, renderer.info.render.calls);
      (window as unknown as { __vol: unknown }).__vol = mesures;
    };
    // ── La taille, le défilement, le vol ──
    const tailler = () => { const w = el.clientWidth, h = el.clientHeight; renderer.setSize(w, h, false); camera.aspect = w / Math.max(1, h); camera.fov = w < h ? 78 : 62; camera.updateProjectionMatrix(); };
    tailler();
    const obsTaille = new ResizeObserver(tailler); obsTaille.observe(el);
    let cible = 0, courant = 0, visible = false, image = 0, vu = -1;
    const lire = () => {
      const r = sec.getBoundingClientRect();
      cible = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - window.innerHeight)));
    };
    lire();
    window.addEventListener('scroll', lire, { passive: true });
    const obsVue = new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) { cancelAnimationFrame(image); image = requestAnimationFrame(dessiner); } });
    obsVue.observe(sec);
    const horloge = new THREE.Clock();
    const teinte = new THREE.Color(), brume = new THREE.Color('#0a1410'), couleurLampe = new THREE.Color();
    function dessiner() {
      if (!visible) return;
      const t = horloge.getElapsedTime();
      courant += (cible - courant) * .07;                                  // le vol suit le doigt en douceur
      const z = DEPART + (ARRIVEE - DEPART) * courant;
      // dans le muscle, le vol se fait droit : on plonge au centre de chaque étape
      const a = THREE.MathUtils.smoothstep(z, DEBUT_ZOOM - 8, DEBUT_ZOOM + 22);
      camera.position.set(Math.sin(courant * 12) * 3.2 * a, Math.sin(courant * 8 + 1) * 1.8 * a + Math.sin(t * .5) * .35, z);
      camera.lookAt(Math.sin(courant * 12 + .6) * 4.5 * a, Math.sin(courant * 8 + 1.4) * 1.2 * a, z - 22);
      camera.rotation.z += Math.cos(courant * 12) * .07 * a;               // il s'incline dans les virages
      lampe.position.set(camera.position.x, camera.position.y + 3, z - 10);
      // la brume prend un peu de la couleur du monde traversé : c'est ce qui fait le rêve
      const proche = MONDES.reduce((m, b) => (Math.abs(b.z - (z - 20)) < Math.abs(m.z - (z - 20)) ? b : m));
      teinte.set(proche.couleur).lerp(brume, .9);
      (scene.fog as THREE.FogExp2).color.lerp(teinte, .04);
      lampe.color.lerp(couleurLampe.set(proche.couleur), .05);
      const t0 = performance.now();
      for (const a of animations) if (a.z === null || (z - a.z < 120 && z - a.z > -20)) a.f(t, z);
      const t1 = performance.now();
      renderer.render(scene, camera);
      if (import.meta.env.DEV) mesurer(t1 - t0, performance.now() - t1, z);
      const arrondi = Math.round(courant * 400) / 400;
      if (arrondi !== vu) { vu = arrondi; setP(arrondi); }
      image = requestAnimationFrame(dessiner);
    }
    const perdu = (ev: Event) => { ev.preventDefault(); setEchec(true); };
    renderer.domElement.addEventListener('webglcontextlost', perdu);

    return () => {
      cancelAnimationFrame(image);
      window.removeEventListener('scroll', lire);
      obsVue.disconnect(); obsTaille.disconnect();
      renderer.domElement.removeEventListener('webglcontextlost', perdu);
      jeter.forEach(x => x.dispose());
      renderer.dispose(); renderer.domElement.remove();
    };
  }, []);

  // La caméra et le monde qu'elle regarde (20 unités devant elle).
  const cz = DEPART + (ARRIVEE - DEPART) * p;
  const z = cz - 20;
  const fin = p > .992;
  const zoom = cz < DEBUT_ZOOM + 6 && !fin;
  const etape = Math.max(0, ETAPES.findIndex(e => e.z < cz - 3));

  // ── La voix du vol : la piste du monde traversé part quand on y entre ──
  // Les navigateurs n'autorisent le son qu'après un geste (un clic, un toucher) : le bouton de la visite guidée le
  // donne ; sans geste, le vol reste muet et un bouton propose d'écouter à la fin.
  const voix = useRef<HTMLAudioElement>(null);
  const [refusee, setRefusee] = useState(false);
  const [visite, setVisite] = useState(false);
  const enCours = useRef(-1);
  const durees = useRef<number[]>(VOIX_VOL.map(v => v.sans));
  useEffect(() => {
    VOIX_VOL.forEach((v, k) => {
      const a = new Audio(); a.preload = 'metadata'; a.src = VOIX_URL(v.fichier);
      a.onloadedmetadata = () => { if (isFinite(a.duration)) durees.current[k] = a.duration; };
    });
  }, []);
  const segment = VOIX_VOL.findIndex(v => p >= v.de && p < v.a);
  useEffect(() => {
    const a = voix.current;
    if (!a || segment === enCours.current) return;
    enCours.current = segment;
    if (segment < 0) { a.pause(); return; }
    a.src = VOIX_URL(VOIX_VOL[segment].fichier);
    a.play().then(() => setRefusee(false)).catch(err => { if (err?.name === 'NotAllowedError') setRefusee(true); });
  }, [segment]);
  /** Rejouer la piste du moment (le geste de l'élève autorise le son). */
  const ecouter = () => { const a = voix.current; if (a) { a.currentTime = 0; a.play().then(() => setRefusee(false)).catch(() => {}); } };

  // ── La visite guidée : le vol défile seul, chaque monde le temps de sa voix ; un geste de l'élève la rend ──
  useEffect(() => {
    if (!visite) return;
    const sec = section.current;
    if (!sec) return;
    let q = Math.max(0, cible()), avant = performance.now();
    function cible() { const r = sec!.getBoundingClientRect(); return Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight))); }
    // une horloge plutôt que requestAnimationFrame : le rythme suit la voix même si l'image ralentit
    const pas = () => {
      const maintenant = performance.now(), dt = Math.min(1.2, (maintenant - avant) / 1000); avant = maintenant;
      const k = Math.max(0, VOIX_VOL.findIndex(v => q >= v.de && q < v.a));
      const v = VOIX_VOL[k];
      q = Math.min(1, q + (v.a - v.de) / (durees.current[k] + .8) * dt);
      window.scrollTo(0, sec.offsetTop + q * (sec.offsetHeight - innerHeight));
      if (q >= 1) setVisite(false);
    };
    const horloge = setInterval(pas, 40);
    const rendre = () => setVisite(false);
    window.addEventListener('wheel', rendre, { passive: true });
    window.addEventListener('touchstart', rendre, { passive: true });
    window.addEventListener('keydown', rendre);
    return () => { clearInterval(horloge); window.removeEventListener('wheel', rendre); window.removeEventListener('touchstart', rendre); window.removeEventListener('keydown', rendre); };
  }, [visite]);
  const lancerVisite = () => {
    const a = voix.current;
    if (a) { enCours.current = 0; a.src = VOIX_URL(VOIX_VOL[0].fichier); a.play().catch(() => {}); }
    setRefusee(false); setVisite(true);
  };

  return (
    <section ref={section} id="vol" className="relative z-10" style={{ height: `${ECRANS * 100}vh` }} aria-label="Survol des matières en 3D">
      <div className="sticky top-0 h-screen overflow-hidden">
        <div ref={hote} className="absolute inset-0 [&>canvas]:w-full [&>canvas]:h-full" />
        {echec && <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,#16302a,#0a1410)]" />}
        <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_center,transparent_45%,#0a1410_100%)]" />

        {/* L'invitation, au départ : c'est la première chose que voit l'élève */}
        <div className="absolute inset-x-0 top-[17vh] [@media(max-height:500px)]:top-[19vh] text-center px-4 transition-opacity duration-500" style={{ opacity: p < .03 && !visite ? 1 : 0, pointerEvents: p < .03 && !visite ? 'auto' : 'none' }}>
          <div className="craie text-2xl [@media(max-height:500px)]:text-lg text-cyan-300 mb-2">— ferme les yeux une seconde —</div>
          <h1 className="craie text-5xl sm:text-7xl [@media(max-height:500px)]:text-4xl text-white leading-[.95]">Imagine ton année<br /><span className="text-yellow-300">vue d'en haut.</span></h1>
          <button onClick={lancerVisite}
            className="lp-ecoute mt-6 [@media(max-height:500px)]:mt-3 inline-flex items-center gap-2 pl-4 pr-5 py-2.5 [@media(max-height:500px)]:py-1.5 rounded-full bg-yellow-300 text-black font-bold text-base hover:bg-yellow-200 transition-colors">
            ▶ Visite guidée avec la voix de Moalim
          </button>
          <p className="text-white/65 mt-3 [@media(max-height:500px)]:mt-1.5 text-sm">ou fais défiler toi-même ↓ · <a href="#accueil" className="underline underline-offset-4 text-white/45 hover:text-white/80">passer le survol</a></p>
        </div>

        {/* Le nom de chaque monde, quand on y entre */}
        {MONDES.map((m, k) => {
          const d = Math.abs(m.z - z), o = fin ? 0 : Math.max(0, 1 - d / 38);
          return (
            <div key={m.nom} className={`absolute top-[13vh] px-5 max-w-md ${k % 2 ? 'right-[4vw] text-right' : 'left-[4vw]'}`}
              style={{ opacity: o, transform: `translateY(${(1 - o) * 26}px)` }}>
              <div className="craie text-6xl sm:text-8xl [@media(max-height:500px)]:text-5xl leading-none" style={{ color: m.couleur, textShadow: `0 0 34px ${m.couleur}66` }}>{m.nom}</div>
              <p className="text-white/80 text-base sm:text-lg [@media(max-height:500px)]:text-[15px] mt-2 leading-snug">{m.phrase}</p>
            </div>
          );
        })}

        {/* Le zoom dans le muscle : où l'on est */}
        <div className="absolute inset-x-0 top-[13vh] [@media(max-height:500px)]:top-[17vh] flex flex-col items-center gap-2 px-4 transition-opacity duration-500 pointer-events-none" style={{ opacity: zoom ? 1 : 0 }}>
          <div className="craie text-xl sm:text-2xl text-green-300">On zoome dans le muscle…</div>
          <div className="flex flex-wrap justify-center items-center gap-x-1.5 gap-y-1 text-[15px] sm:text-base">
            {ETAPES.map((e, k) => (
              <span key={e.nom} className="craie transition-colors duration-300" style={{ color: k === etape ? '#4ade80' : k < etape ? 'rgba(226,232,240,.75)' : 'rgba(226,232,240,.3)' }}>
                {k > 0 && <span className="text-white/30 mr-1.5">›</span>}{e.nom}
              </span>
            ))}
          </div>
        </div>

        {/* Le réveil : Moalim le dit en darija, la phrase est écrite en dessous en français */}
        <audio ref={voix} preload="auto" />
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-4 transition-opacity duration-700 bg-[radial-gradient(ellipse_at_center,rgba(10,20,16,.93)_0%,rgba(10,20,16,.82)_60%,rgba(10,20,16,.6)_100%)]" style={{ opacity: fin ? 1 : 0, pointerEvents: fin ? 'auto' : 'none' }}>
          {/* En darija seulement (26 novembre 2026) ; les mots clés s'allument et se soulignent comme dans « le mot de Moalim » */}
          <div dir="rtl" className={`font-brand font-bold text-white max-w-4xl ${fin ? 'lp-mots-vus' : ''}`}>
            <p className="text-4xl sm:text-6xl [@media(max-height:500px)]:text-3xl leading-[1.35]">
              هادشي ماشي حلم، هادا هو <span className="lp-mot" style={MOT('#fde047', 0)}>البرنامج ديالك</span>.
            </p>
            <p className="mt-3 [@media(max-height:500px)]:mt-1 text-2xl sm:text-4xl [@media(max-height:500px)]:text-xl leading-[1.5] text-white/90">
              غادي نقطعوه <span className="lp-mot" style={MOT('#6ee7b7', 1)}>مع بعض</span>، درس بدرس، وأنا معاك فكل خطوة.
            </p>
            <p className="mt-3 [@media(max-height:500px)]:mt-1 text-3xl sm:text-5xl [@media(max-height:500px)]:text-2xl leading-[1.4]">
              <span className="lp-mot" style={MOT('#fde047', 2)}>يالاه نبداو!</span> ↓
            </p>
          </div>
          {refusee && (
            <button onClick={ecouter} className="mt-4 [@media(max-height:500px)]:mt-2 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-yellow-300 text-black font-bold text-sm hover:bg-yellow-200 transition-colors">
              ▶ Écouter Moalim
            </button>
          )}
        </div>

        {/* Le tuteur vole devant : il penche et monte avec le vol */}
        <img src="/media/avatar/moalim-professeur.png" alt="" draggable={false}
          className="absolute left-1/2 bottom-[3vh] w-28 sm:w-36 [@media(max-height:500px)]:w-20 pointer-events-none select-none drop-shadow-[0_18px_30px_rgba(0,0,0,.6)]"
          style={{ transform: `translateX(calc(-50% + ${Math.sin(p * 12) * 14 * (zoom ? .3 : 1)}vw)) rotate(${Math.cos(p * 12) * 13 * (zoom ? .3 : 1)}deg)`, opacity: fin ? 0 : 1, transition: 'opacity .5s' }} />

        {/* Le son refusé en plein vol (pas encore de geste) : une petite invitation */}
        {refusee && !fin && p > .03 && (
          <button onClick={ecouter} className="absolute right-3 top-20 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-yellow-300 text-black font-bold text-sm shadow-xl hover:bg-yellow-200">
            🔊 Écouter Moalim
          </button>
        )}

        {/* Le chemin parcouru */}
        <div className="absolute left-1/2 -translate-x-1/2 bottom-3 flex items-center gap-2">
          {MONDES.map(m => (
            <span key={m.nom} className="h-1.5 w-8 sm:w-12 rounded-full transition-colors duration-500"
              style={{ background: z <= m.z + 30 ? m.couleur : 'rgba(226,232,240,.2)' }} />
          ))}
        </div>
      </div>
    </section>
  );
}
