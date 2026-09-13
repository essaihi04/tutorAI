import * as THREE from 'three';

export const STRUCTURE_LEVELS = [
  { step: 0, name: 'Muscle', detail: 'Un organe constitué de faisceaux, relié aux os par les tendons.', remember: 'Le muscle contient plusieurs faisceaux.' },
  { step: 1, name: 'Faisceau', detail: 'Un paquet de fibres entouré de périmysium, un tissu conjonctif.', remember: 'Un faisceau contient plusieurs cellules musculaires.' },
  { step: 2, name: 'Fibre', detail: 'Une seule cellule longue, avec plusieurs noyaux périphériques et de nombreuses myofibrilles.', remember: 'Fibre musculaire = cellule musculaire.' },
  { step: 3, name: 'Myofibrille', detail: 'Un cylindre contractile où les sarcomères se répètent de strie Z en strie Z.', remember: 'Une myofibrille est une succession de sarcomères.' },
  { step: 5, name: 'Sarcomère', detail: 'L’unité contractile entre deux stries Z : actine fine et myosine épaisse se chevauchent.', remember: 'Les filaments glissent ; leur longueur reste constante.' },
] as const;
export function disposeMuscleStructure(group: THREE.Group) {
  const materials=new Set<THREE.Material>();
  const textures=new Set<THREE.Texture>();
  group.traverse(object=>{if(object instanceof THREE.Mesh){object.geometry.dispose();(Array.isArray(object.material)?object.material:[object.material]).forEach(m=>materials.add(m));}});
  materials.forEach(m=>{Object.values(m).forEach(value=>{if(value instanceof THREE.Texture)textures.add(value);});m.dispose();});
  textures.forEach(texture=>texture.dispose());
}
