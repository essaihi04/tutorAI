import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { disposeMuscleStructure, STRUCTURE_LEVELS } from './muscleStructureModel';
import './muscleStructure.css';

interface Props { step: number; onStep: (step: number) => void; labels: boolean; }
export default function MuscleStructure3D({step,onStep,labels}:Props) {
  const host=useRef<HTMLDivElement>(null);
  const resetCamera=useRef<()=>void>(()=>{});
  const modelRef=useRef<THREE.Group | null>(null);
  const cutawayRef=useRef(true);
  const [cutaway,setCutaway]=useState(true);
  const [failed,setFailed]=useState(false);
  const [loading,setLoading]=useState(true);
  const [selected,setSelected]=useState('');
  const level=STRUCTURE_LEVELS.find(l=>l.step===step) || STRUCTURE_LEVELS[0];
  const index=STRUCTURE_LEVELS.indexOf(level);
  const [legend,setLegend]=useState<{name:string;color:string}[]>([]);

  useEffect(()=>{
    cutawayRef.current=cutaway;
    modelRef.current?.traverse(object=>{if(object.userData.cover===true)object.visible=!cutaway;});
  },[cutaway]);

  useEffect(()=>{
    const container=host.current;if(!container)return;
    setSelected('');setFailed(false);setLoading(true);
    let renderer:THREE.WebGLRenderer;
    try {renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});} catch {setFailed(true);return;}
    renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.75));
    renderer.outputColorSpace=THREE.SRGBColorSpace;
    renderer.toneMapping=THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure=1.25;
    renderer.setClearColor(0x000000,0);
    container.appendChild(renderer.domElement);
    renderer.domElement.setAttribute('aria-label',`Modèle 3D : ${level.name}. Glisser pour tourner ; molette ou pincement pour zoomer.`);
    renderer.domElement.setAttribute('role','img');
    const scene=new THREE.Scene();
    const group=new THREE.Group();scene.add(group);modelRef.current=group;
    const camera=new THREE.PerspectiveCamera(36,1,.1,100);
    const controls=new OrbitControls(camera,renderer.domElement);
    controls.enableDamping=true;controls.enablePan=false;controls.minDistance=6;controls.maxDistance=22;
    const fitModel=()=>{
      if(!group.children.length)return;
      const bounds=new THREE.Box3().setFromObject(group);
      for(let attempt=0;attempt<20;attempt++){
        camera.updateMatrixWorld();
        let extent=0;
        for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){
          const p=new THREE.Vector3(x,y,z).project(camera);extent=Math.max(extent,Math.abs(p.x),Math.abs(p.y));
        }
        if(extent<=.86)break;
        camera.position.sub(controls.target).multiplyScalar(1.08).add(controls.target);
      }
      controls.maxDistance=Math.max(22,camera.position.length()*1.5);controls.update();
    };
    resetCamera.current=()=>{camera.position.set(5,3.2,8);controls.target.set(0,0,0);controls.update();fitModel();};resetCamera.current();
    scene.add(new THREE.HemisphereLight('#f4f2ed','#343a48',1.5));
    const key=new THREE.DirectionalLight('#fff0df',3.2);key.position.set(-2,5,7);scene.add(key);
    const rim=new THREE.DirectionalLight('#a9c2da',1.7);rim.position.set(3,2,-5);scene.add(rim);
    let disposed=false;
    const file=({0:'muscle',1:'fascicle',2:'fiber',3:'myofibril',5:'sarcomere'} as Record<number,string>)[step];
    new GLTFLoader().load(`/media/models/svt/muscle/${file}.glb`,gltf=>{
      if(disposed){disposeMuscleStructure(gltf.scene);return;}
      gltf.scene.traverse(object=>{
        if(object.userData.cover===true)object.visible=!cutawayRef.current;
        if(object instanceof THREE.Mesh){
          const materials=Array.isArray(object.material)?object.material:[object.material];
          materials.forEach(material=>{if(material instanceof THREE.MeshStandardMaterial){material.side=THREE.DoubleSide;material.metalness=0;}});
        }
      });
      group.add(gltf.scene);fitModel();setLoading(false);
    },undefined,()=>{if(!disposed){setLoading(false);setFailed(true);}});
    const legends:Record<number,{name:string;color:string}[]>={
      0:[{name:'Tendon',color:'#dfd0ad'},{name:'Faisceaux',color:'#b05253'},{name:'Épimysium',color:'#87383d'}],
      1:[{name:'Fibres musculaires',color:'#b05253'},{name:'Périmysium',color:'#c29180'},{name:'Endomysium',color:'#dfd0ad'}],
      2:[{name:'Sarcolemme',color:'#c29180'},{name:'Noyaux périphériques',color:'#795776'},{name:'Myofibrilles',color:'#a05d5d'},{name:'Réticulum',color:'#98804e'}],
      3:[{name:'Stries Z',color:'#b09061'},{name:'Bandes A',color:'#87383d'},{name:'Myofilaments',color:'#a05d5d'}],
      5:[{name:'Stries Z',color:'#b09061'},{name:'Actine',color:'#b84433'},{name:'Myosine',color:'#336178'}],
    };setLegend(legends[step]);
    const resize=()=>{const {width,height}=container.getBoundingClientRect();if(!width||!height)return;renderer.setSize(width,height);camera.aspect=width/height;camera.updateProjectionMatrix();fitModel();};
    const observer=new ResizeObserver(resize);observer.observe(container);resize();
    let frame=0;
    const render=()=>{controls.update();renderer.render(scene,camera);frame=requestAnimationFrame(render);};render();
    const raycaster=new THREE.Raycaster();let down=[0,0];
    const pointerDown=(e:PointerEvent)=>{down=[e.clientX,e.clientY];};
    const pointerUp=(e:PointerEvent)=>{if(Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;const r=renderer.domElement.getBoundingClientRect();raycaster.setFromCamera(new THREE.Vector2((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1),camera);const hit=raycaster.intersectObject(group,true).find(hit=>{let object:THREE.Object3D|null=hit.object;while(object){if(!object.visible)return false;object=object.parent;}return true;});let object=hit?.object;while(object&&!object.userData.anatomical_label)object=object.parent||undefined;setSelected(object?.userData.anatomical_label || '');};
    const lost=(event:Event)=>{event.preventDefault();setFailed(true);cancelAnimationFrame(frame);};
    renderer.domElement.addEventListener('pointerdown',pointerDown);renderer.domElement.addEventListener('pointerup',pointerUp);renderer.domElement.addEventListener('webglcontextlost',lost);
    return ()=>{disposed=true;modelRef.current=null;cancelAnimationFrame(frame);observer.disconnect();controls.dispose();disposeMuscleStructure(group);renderer.domElement.removeEventListener('pointerdown',pointerDown);renderer.domElement.removeEventListener('pointerup',pointerUp);renderer.domElement.removeEventListener('webglcontextlost',lost);renderer.dispose();renderer.domElement.remove();resetCamera.current=()=>{};};
  },[step,level.name]);

  return <figure className="muscle-structure" data-scientific-engine="three" data-scientific-model="muscle_excitation_contraction" data-stage-index={step} data-stage={['muscle','fascicle','muscle_fiber','myofibril','','sarcomere'][step]} data-renderer="blender-gltf" data-model-loaded={!loading&&!failed}>
    <header><h3>{level.name}</h3><p>{level.remember}</p></header>
    <div className="structure-scene">
      <div ref={host} className="structure-canvas" onDoubleClick={()=>resetCamera.current()} title="Glisser pour tourner, pincer pour zoomer, double-cliquer pour recentrer" />
      {loading&&!failed&&<div className="structure-loading" role="status">Chargement du modèle…</div>}
      {failed&&<div className="structure-fallback"><img src="/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/hierarchie_muscle_3d.png" alt="Muscle, faisceau, fibre et myofibrille : agrandissements successifs"/><p>Vue illustrée : la 3D est indisponible sur cet appareil.</p></div>}
      <output className="structure-selected" aria-live="polite">{selected?`Élément touché : ${selected}`:''}</output>
    </div>
    <div className="structure-bottom">
      {labels&&<div className="structure-legend" aria-label="Légende">{legend.map(l=><span key={l.name}><i style={{background:l.color}}/>{l.name}</span>)}</div>}
      <div className="structure-navigation" aria-label="Explorer les niveaux">
        <button onClick={()=>onStep(STRUCTURE_LEVELS[Math.max(0,index-1)].step)} disabled={index===0} aria-label="Niveau précédent">←</button>
        <span>{index+1} / 5</span>
        {step<3&&<button onClick={()=>setCutaway(v=>!v)} aria-pressed={cutaway}>{cutaway?'Fermer la coupe':'Ouvrir la coupe'}</button>}
        <button onClick={()=>onStep(index<4?STRUCTURE_LEVELS[index+1].step:6)} aria-label={index<4?'Niveau suivant':'Continuer vers le couplage'}>→</button>
      </div>
      <small>Glisser pour tourner · Pincer / molette pour zoomer · Modèle sans échelle commune</small>
    </div>
  </figure>;
}
