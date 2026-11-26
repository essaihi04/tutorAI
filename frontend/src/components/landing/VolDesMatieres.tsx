import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

/**
 * Le vol au-dessus des matières (26 novembre 2026, « quand l'élève scrolle, une revue en 3D des matières, comme s'il
 * vole au-dessus de la physique, des maths, des SVT — comme un rêve »).
 *
 * Une section haute (une hauteur d'écran par matière) dont la scène reste collée à l'écran : le défilement est la
 * manette. La caméra avance dans un ciel de poussière de craie et traverse quatre mondes — une surface et des courbes
 * (maths), un atome et une onde (physique), une molécule (chimie), une double hélice d'ADN (SVT). Le tuteur vole
 * devant, les titres apparaissent quand on entre dans chaque monde.
 *
 * Rien ne tourne hors de l'écran ; la scène ne dessine que ce que three.js sait déjà (pas de modèle à télécharger).
 */

const MONDES = [
  { z: -60, couleur: '#facc15', nom: 'Les maths', phrase: 'Les courbes prennent vie : limites, dérivées, suites, complexes.', signes: ['f ′(x)', '∫', 'lim', 'uₙ', 'ln x', 'π', 'z = a + ib'] },
  { z: -150, couleur: '#22d3ee', nom: 'La physique', phrase: 'Tu vois l\'onde avancer, le condensateur se charger, le noyau se désintégrer.', signes: ['λ', 'τ = RC', 'v = λ·f', 'E = mc²', 'T₀', 'u_C'] },
  { z: -240, couleur: '#fb923c', nom: 'La chimie', phrase: 'Les molécules se rencontrent : vitesse, équilibre, pH, dosage.', signes: ['pH', 'Qr', 'K', 'H₃O⁺', 'pKa', 'x_max'] },
  { z: -330, couleur: '#4ade80', nom: 'Les SVT', phrase: 'Tu entres dans la cellule : ADN, protéines, muscle, énergie.', signes: ['ADN', 'ATP', 'ARNm', 'codon', 'Ca²⁺', 'glucose'] },
] as const;
const DEPART = 20, ARRIVEE = -318;

/** Un signe écrit à la craie, sur une petite toile : il flotte dans le monde de sa matière. */
function signe(texte: string, couleur: string) {
  const toile = document.createElement('canvas');
  toile.width = 512; toile.height = 160;
  const c = toile.getContext('2d')!;
  c.font = "92px 'Patrick Hand','Caveat','Segoe Print',cursive";
  c.textAlign = 'center'; c.textBaseline = 'middle';
  c.shadowColor = couleur; c.shadowBlur = 18; c.fillStyle = couleur;
  c.fillText(texte, 256, 84);
  const texture = new THREE.CanvasTexture(toile);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, transparent: true, depthWrite: false, opacity: .9 }));
  s.scale.set(9, 2.8, 1);
  return s;
}

const hasard = (a: number, b: number) => a + Math.random() * (b - a);

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
    el.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0a1410, 0.018);
    const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 260);
    scene.add(new THREE.AmbientLight(0xffffff, 0.9));
    const lampe = new THREE.PointLight(0xffffff, 60, 90); scene.add(lampe);

    const jeter: { dispose(): void }[] = [];
    const garde = <T extends { dispose(): void }>(x: T) => { jeter.push(x); return x; };
    const anime: ((t: number) => void)[] = [];
    const fil = (couleur: string, opacity = .9) => garde(new THREE.LineBasicMaterial({ color: couleur, transparent: true, opacity }));
    const mat = (couleur: string, opacity = 1) => garde(new THREE.MeshStandardMaterial({ color: couleur, emissive: couleur, emissiveIntensity: .55, roughness: .4, transparent: opacity < 1, opacity }));

    // ── La poussière de craie : tout le long du vol ──
    {
      const n = petit ? 900 : 2200, pos = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) { pos[i * 3] = hasard(-70, 70); pos[i * 3 + 1] = hasard(-40, 40); pos[i * 3 + 2] = hasard(ARRIVEE - 90, DEPART + 10); }
      const g = garde(new THREE.BufferGeometry()); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      const m = garde(new THREE.PointsMaterial({ color: 0xe2e8f0, size: .32, transparent: true, opacity: .75, depthWrite: false }));
      scene.add(new THREE.Points(g, m));
    }
    // ── Les signes de chaque matière, autour du couloir de vol ──
    for (const monde of MONDES) {
      monde.signes.forEach((txt, k) => {
        const s = signe(txt, monde.couleur);
        const cote = k % 2 ? 1 : -1;
        s.position.set(cote * hasard(9, 22), hasard(-8, 9), monde.z + 34 - k * 11);
        const y0 = s.position.y, d = hasard(0, 6);
        anime.push(t => { s.position.y = y0 + Math.sin(t * .6 + d) * .8; });
        jeter.push(s.material.map!, s.material);
        scene.add(s);
      });
    }

    // ── Maths : une surface qui ondule (z = sin x · cos y) et une parabole ──
    {
      const g = garde(new THREE.PlaneGeometry(64, 64, 32, 32));
      const surface = new THREE.Mesh(g, garde(new THREE.MeshBasicMaterial({ color: '#facc15', wireframe: true, transparent: true, opacity: .28 })));
      surface.rotation.x = -Math.PI / 2; surface.position.set(0, -8, MONDES[0].z);
      const base = g.attributes.position.array.slice() as Float32Array;
      anime.push(t => {
        const a = g.attributes.position.array as Float32Array;
        for (let i = 0; i < a.length; i += 3) a[i + 2] = Math.sin(base[i] * .22 + t * .7) * Math.cos(base[i + 1] * .22) * 2.6;
        g.attributes.position.needsUpdate = true;
      });
      scene.add(surface);
      const pts: THREE.Vector3[] = [];
      for (let x = -9; x <= 9; x += .3) pts.push(new THREE.Vector3(x, x * x * .16 - 4, 0));
      const parabole = new THREE.Line(garde(new THREE.BufferGeometry().setFromPoints(pts)), fil('#facc15'));
      parabole.position.set(8, 1, MONDES[0].z - 4); parabole.rotation.y = -.45; parabole.scale.setScalar(1.25);
      const tangente = new THREE.Line(garde(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-7, 0, 0), new THREE.Vector3(7, 0, 0)])), fil('#fb923c'));
      parabole.add(tangente);
      anime.push(t => { const x = Math.sin(t * .5) * 6; tangente.position.set(x, x * x * .16 - 4, 0); tangente.rotation.z = Math.atan(.32 * x); });
      scene.add(parabole);
    }
    // ── Physique : un atome (noyau, trois orbites, électrons) et une onde qui avance ──
    {
      const atome = new THREE.Group(); atome.position.set(-8, 2, MONDES[1].z); atome.scale.setScalar(1.25);
      atome.add(new THREE.Mesh(garde(new THREE.SphereGeometry(1.5, 24, 16)), mat('#f472b6')));
      const gOrbite = garde(new THREE.TorusGeometry(6, .05, 8, 80)), gElectron = garde(new THREE.SphereGeometry(.42, 16, 12));
      [0, 1, 2].forEach(k => {
        const plan = new THREE.Group(); plan.rotation.set(k * 1.05, k * .7, 0);
        plan.add(new THREE.Mesh(gOrbite, garde(new THREE.MeshBasicMaterial({ color: '#22d3ee', transparent: true, opacity: .55 }))));
        const e = new THREE.Mesh(gElectron, mat('#22d3ee')); plan.add(e);
        anime.push(t => { const a = t * (1.4 + k * .35) + k * 2; e.position.set(Math.cos(a) * 6, Math.sin(a) * 6, 0); });
        atome.add(plan);
      });
      anime.push(t => { atome.rotation.y = t * .25; });
      scene.add(atome);
      const n = 160, pts = new Float32Array(n * 3);
      const g = garde(new THREE.BufferGeometry()); g.setAttribute('position', new THREE.BufferAttribute(pts, 3));
      const onde = new THREE.Line(g, fil('#22d3ee')); onde.position.set(4, -6, MONDES[1].z - 18);
      anime.push(t => {
        for (let i = 0; i < n; i++) { const x = i * .28; pts[i * 3] = x; pts[i * 3 + 1] = Math.sin(x * .9 - t * 3) * 2.2 * Math.exp(-x * .03); pts[i * 3 + 2] = 0; }
        g.attributes.position.needsUpdate = true;
      });
      scene.add(onde);
    }
    // ── Chimie : une molécule qui tourne (boules et liaisons) ──
    {
      const mol = new THREE.Group(); mol.position.set(7.5, 1, MONDES[2].z); mol.scale.setScalar(1.35);
      const atomes: [number, number, number, string, number][] = [[0, 0, 0, '#fb923c', 1.5], [3.4, 1.8, 0, '#f87171', 1.15], [-3.4, 1.8, 0, '#f87171', 1.15], [0, -3.6, 0, '#e2e8f0', .85], [5.6, -.4, 1.5, '#e2e8f0', .7], [-5.6, -.4, -1.5, '#e2e8f0', .7]];
      const gBoule = garde(new THREE.SphereGeometry(1, 24, 16)), mLiaison = garde(new THREE.MeshBasicMaterial({ color: '#e2e8f0', transparent: true, opacity: .5 }));
      atomes.forEach(([x, y, z, c, r]) => { const b = new THREE.Mesh(gBoule, mat(c)); b.scale.setScalar(r); b.position.set(x, y, z); mol.add(b); });
      [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5]].forEach(([a, b]) => {
        const A = new THREE.Vector3(...(atomes[a].slice(0, 3) as [number, number, number])), B = new THREE.Vector3(...(atomes[b].slice(0, 3) as [number, number, number]));
        const l = new THREE.Mesh(garde(new THREE.CylinderGeometry(.16, .16, A.distanceTo(B), 8)), mLiaison);
        l.position.copy(A).add(B).multiplyScalar(.5); l.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), B.clone().sub(A).normalize()); mol.add(l);
      });
      anime.push(t => { mol.rotation.set(Math.sin(t * .3) * .4, t * .45, 0); });
      scene.add(mol);
      // des bulles qui montent, comme dans un bécher
      const gB = garde(new THREE.SphereGeometry(.5, 12, 8)), mB = garde(new THREE.MeshBasicMaterial({ color: '#fb923c', transparent: true, opacity: .35 }));
      for (let k = 0; k < (petit ? 10 : 22); k++) {
        const b = new THREE.Mesh(gB, mB); const x = hasard(-18, 4), z = MONDES[2].z + hasard(-22, 22), v = hasard(.8, 2), d = hasard(0, 30);
        b.scale.setScalar(hasard(.4, 1.3));
        anime.push(t => { b.position.set(x + Math.sin(t + d) * .6, ((t * v + d) % 30) - 15, z); });
        scene.add(b);
      }
    }
    // ── SVT : la double hélice d'ADN, couchée le long du vol ──
    {
      const adn = new THREE.Group(); adn.position.set(-6, 0, MONDES[3].z - 4); adn.rotation.z = .35; adn.scale.setScalar(1.25);
      const gBase = garde(new THREE.SphereGeometry(.55, 14, 10)), paires = ['#4ade80', '#facc15', '#22d3ee', '#f472b6'];
      const mBarreau = garde(new THREE.MeshBasicMaterial({ color: '#e2e8f0', transparent: true, opacity: .4 }));
      const gBarreau = garde(new THREE.CylinderGeometry(.09, .09, 6, 6));
      for (let k = 0; k < 34; k++) {
        const a = k * .42, y = (k - 17) * 1.15;
        const A = new THREE.Mesh(gBase, mat(paires[k % 4])), B = new THREE.Mesh(gBase, mat(paires[(k + 2) % 4]));
        A.position.set(Math.cos(a) * 3, y, Math.sin(a) * 3); B.position.set(-Math.cos(a) * 3, y, -Math.sin(a) * 3);
        const barreau = new THREE.Mesh(gBarreau, mBarreau); barreau.position.set(0, y, 0); barreau.rotation.set(0, -a, Math.PI / 2);
        adn.add(A, B, barreau);
      }
      anime.push(t => { adn.rotation.y = t * .35; });
      scene.add(adn);
      // des cellules translucides
      const gC = garde(new THREE.SphereGeometry(1, 20, 14));
      for (let k = 0; k < (petit ? 5 : 10); k++) {
        const c = new THREE.Mesh(gC, garde(new THREE.MeshStandardMaterial({ color: '#4ade80', transparent: true, opacity: .16, roughness: .2 })));
        c.scale.setScalar(hasard(1.6, 4)); c.position.set(hasard(4, 26), hasard(-10, 10), MONDES[3].z + hasard(-26, 24));
        const noyau = new THREE.Mesh(gC, mat('#4ade80', .5)); noyau.scale.setScalar(.3); c.add(noyau);
        const y0 = c.position.y, d = hasard(0, 6);
        anime.push(t => { c.position.y = y0 + Math.sin(t * .4 + d) * 1.2; });
        scene.add(c);
      }
    }

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
    const teinte = new THREE.Color(), brume = new THREE.Color('#0a1410');
    function dessiner() {
      if (!visible) return;
      const t = horloge.getElapsedTime();
      courant += (cible - courant) * .07;                                  // le vol suit le doigt en douceur
      const z = DEPART + (ARRIVEE - DEPART) * courant;
      camera.position.set(Math.sin(courant * 9) * 3.2, Math.sin(courant * 6 + 1) * 1.8 + Math.sin(t * .5) * .35, z);
      camera.lookAt(Math.sin(courant * 9 + .6) * 4.5, Math.sin(courant * 6 + 1.4) * 1.2, z - 22);
      camera.rotation.z += Math.cos(courant * 9) * .07;                    // il s'incline dans les virages
      lampe.position.set(camera.position.x, camera.position.y + 3, z - 10);
      // la brume prend un peu de la couleur du monde traversé : c'est ce qui fait le rêve
      const proche = MONDES.reduce((a, b) => (Math.abs(b.z - (z - 20)) < Math.abs(a.z - (z - 20)) ? b : a));
      teinte.set(proche.couleur).lerp(brume, .9);
      (scene.fog as THREE.FogExp2).color.lerp(teinte, .04);
      lampe.color.lerp(new THREE.Color(proche.couleur), .05);
      for (const f of anime) f(t);
      renderer.render(scene, camera);
      const arrondi = Math.round(courant * 200) / 200;
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

  // Le monde traversé : la caméra regarde 20 unités devant elle.
  const z = DEPART + (ARRIVEE - DEPART) * p - 20;
  const fin = p > .975;

  return (
    <section ref={section} id="vol" className="relative z-10" style={{ height: `${(MONDES.length + 1.4) * 100}vh` }} aria-label="Survol des matières en 3D">
      <div className="sticky top-0 h-screen overflow-hidden">
        <div ref={hote} className="absolute inset-0 [&>canvas]:w-full [&>canvas]:h-full" />
        {echec && <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,#16302a,#0a1410)]" />}
        <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_center,transparent_45%,#0a1410_100%)]" />

        {/* L'invitation, au départ */}
        <div className="absolute inset-x-0 top-[16vh] text-center px-4 transition-opacity duration-500" style={{ opacity: p < .05 ? 1 : 0 }}>
          <div className="craie text-2xl text-cyan-300 mb-2">— ferme les yeux une seconde —</div>
          <h2 className="craie text-5xl sm:text-7xl text-white leading-[.95]">Imagine ton année<br /><span className="text-yellow-300">vue d'en haut.</span></h2>
          <p className="text-white/60 mt-4 text-sm sm:text-base">Fais défiler : Moalim t'emmène survoler tes matières ↓</p>
        </div>

        {/* Le nom de chaque monde, quand on y entre */}
        {MONDES.map((m, k) => {
          const d = Math.abs(m.z - z), o = fin ? 0 : Math.max(0, 1 - d / 34);
          return (
            <div key={m.nom} className={`absolute top-[14vh] px-5 max-w-md ${k % 2 ? 'right-[4vw] text-right' : 'left-[4vw]'}`}
              style={{ opacity: o, transform: `translateY(${(1 - o) * 26}px)` }}>
              <div className="craie text-6xl sm:text-8xl leading-none" style={{ color: m.couleur, textShadow: `0 0 34px ${m.couleur}66` }}>{m.nom}</div>
              <p className="text-white/80 text-base sm:text-lg mt-2 leading-snug">{m.phrase}</p>
            </div>
          );
        })}

        {/* Le réveil */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-4 transition-opacity duration-500" style={{ opacity: fin ? 1 : 0 }}>
          <h2 className="craie text-5xl sm:text-7xl text-white leading-[.95]">Ce n'est pas un rêve.<br /><span className="text-yellow-300">C'est ton programme.</span></h2>
          <p className="text-white/70 mt-4 max-w-md">Et on va le traverser ensemble, notion après notion.</p>
        </div>

        {/* Le tuteur vole devant : il penche et monte avec le vol */}
        <img src="/media/avatar/moalim-professeur.png" alt="" draggable={false}
          className="lp-vole absolute left-1/2 bottom-[3vh] w-28 sm:w-36 pointer-events-none select-none drop-shadow-[0_18px_30px_rgba(0,0,0,.6)]"
          style={{ transform: `translateX(calc(-50% + ${Math.sin(p * 9) * 14}vw)) rotate(${Math.cos(p * 9) * 13}deg)`, opacity: fin ? 0 : 1, transition: 'opacity .5s' }} />

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
