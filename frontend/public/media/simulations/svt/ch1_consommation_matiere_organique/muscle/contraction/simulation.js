'use strict';
// Contraction musculaire — sarcomère dessiné à la craie (kit shared/tableau/tableau.js).
const CONFIG={id:'svt_ch1_contraction_actine_myosine',variants:[{id:'ca_atp',label:'Ca²⁺ et ATP'},{id:'sans_ca',label:'Sans Ca²⁺'},{id:'sans_atp',label:'Sans ATP'},{id:'sans_ca_atp',label:'Sans Ca²⁺ ni ATP'}],objectives:['Distinguer les rôles de Ca²⁺ et ATP et observer le glissement à longueur de filament constante.'],commands:['start','set_variant','set_parameters','reset','replay','next','highlight']};
window.SIMULATION_CONFIG=CONFIG;
const {Craie,ecrire,bulle,appuyer}=window.Tableau;
// Script d'explication : le tuteur dit chaque phrase pendant que le professeur montre le repère du doigt.
const EXPLICATION={
 ca_atp:[{repere:'stries_z',texte:'Le sarcomère est limité par deux stries Z.'},{repere:'actine',texte:'Les filaments fins d’actine sont accrochés aux stries Z.'},{repere:'myosine',texte:'Au centre, le filament épais de myosine porte des têtes mobiles.'},{repere:'tropomyosine',texte:'Avec Ca²⁺, la tropomyosine se déplace et libère les sites de fixation de l’actine.'},{repere:'tetes_myosine',texte:'Les têtes s’accrochent, pivotent et tirent l’actine vers le centre ; un nouvel ATP les détache et son hydrolyse les réarme.'},{repere:'cote_zz',texte:'Les stries Z se rapprochent : le sarcomère raccourcit alors que chaque filament garde sa longueur.'}],
 sans_ca:[{repere:'tropomyosine',texte:'Sans Ca²⁺, la tropomyosine masque les sites de fixation de l’actine.'},{repere:'tetes_myosine',texte:'Les têtes de myosine, même armées, ne peuvent pas s’accrocher.'},{repere:'cote_zz',texte:'Aucun glissement : la distance Z–Z ne change pas.'}],
 sans_atp:[{repere:'tetes_myosine',texte:'Les têtes déjà armées s’accrochent à l’actine et tirent une fois…'},{repere:'myosine',texte:'…mais sans nouvel ATP, le pont actine–myosine ne peut pas se détacher.'},{repere:'cote_zz',texte:'Le cycle est bloqué : pas de contraction répétée, le muscle reste rigide.'}],
 sans_ca_atp:[{repere:'tropomyosine',texte:'Sans Ca²⁺, les sites de l’actine restent masqués.'},{repere:'tetes_myosine',texte:'Et sans ATP, aucun pont formé ne pourrait se détacher.'},{repere:'cote_zz',texte:'Le sarcomère reste immobile.'}]};
window.Tableau.explication(EXPLICATION);
const S={calcium:true,atp:true,status:'idle',step:0,completed:new Set(),actions:[],timer:null,ouvert:performance.now(),marques:{},shift:0,shiftFrom:0,shiftTo:0,t0:0,dirty:true};
const $=id=>document.getElementById(id);
const steps=[['Prédis le résultat','Avec Ca²⁺ et ATP, les cycles peuvent se répéter. Que se passe-t-il si tu retires l’un des deux ?'],['Le calcium autorise la liaison','Le Ca²⁺ se fixe à la troponine. La tropomyosine se déplace : les sites de l’actine deviennent accessibles.'],['La myosine s’accroche','Une tête déjà armée, portant ADP et Pi, se lie à un site accessible de l’actine.'],['La tête pivote et tire l’actine','La libération de Pi accompagne le coup de force, puis l’ADP est libéré. Les stries Z se rapprochent ; les filaments gardent leur longueur.'],['Un nouvel ATP détache la tête','La fixation d’un nouvel ATP sur la myosine rompt le pont avec l’actine. Fixation et hydrolyse sont deux étapes différentes.'],['L’hydrolyse réarme la tête','ATP + H₂O → ADP + Pi. L’énergie libérée réarme la myosine. Un autre cycle devient possible si le Ca²⁺ reste disponible.']];
function variant(){return S.calcium?(S.atp?'ca_atp':'sans_atp'):(S.atp?'sans_ca':'sans_ca_atp')}
function stop(){clearTimeout(S.timer);S.timer=null}
function action(name){S.actions.push({action:name,variant:variant(),step:S.step});S.actions=S.actions.slice(-24)}
function texteEtape(){
 let [title,text]=steps[S.step];
 if(S.step>0&&!S.calcium){title='Sites masqués : aucun nouveau pont';text=S.atp?'Même avec ATP, l’absence de Ca²⁺ empêche l’accès aux sites de l’actine. Aucun glissement dans cet essai.':'Sans Ca²⁺, aucun nouveau pont ne se forme ici. Sans ATP, des ponts déjà fixés ne pourraient pas se détacher.'}
 else if(S.step===2&&!S.atp){title='Pont fixé : le cycle est bloqué';text='La tête était déjà armée au départ. Sans nouvel ATP, un pont formé ne peut pas se détacher. Ce modèle montre le blocage, pas une contraction répétée.'}
 return [title,text];
}
function render(){
 $('calcium').checked=S.calcium;$('atp').checked=S.atp;
 const shift=S.step>=3?40:0;
 if(shift!==S.shiftTo){S.shiftFrom=S.shift;S.shiftTo=shift;S.t0=performance.now()}
 $('length').textContent=`Distance Z–Z : ${Math.round((680-2*shift)/680*100)} % de la longueur initiale`;
 $('bands').textContent=shift?'diminuent':'au repos';
 const [title,text]=texteEtape();
 ecrire($('title'),title);ecrire($('text'),text,{vitesse:50});$('step').textContent=S.step?`ÉTAPE ${S.step} / 5`:'AVANT L’ESSAI';
 $('status').textContent={idle:'Prêt',running:'Observation',finished:'Essai terminé'}[S.status];
 $('run').textContent=S.status==='finished'?'Rejouer':'Animer';
 $('coverage').textContent=`${S.completed.size} / 4 conditions observées`;
 const cle=`${variant()}-${S.step}`;if(S.marques[cle]==null)S.marques[cle]=(performance.now()-S.ouvert)/1000;
 S.dirty=true;
}
function emit(){window.parent.postMessage({type:'simulation_state',simulation_id:CONFIG.id,student_actions:S.actions,current_state:{simulation_status:S.status,current_variant:variant(),variants_completed:[...S.completed],calcium_present:S.calcium,atp_present:S.atp,cycle_step:S.step,sarcomere_shortening:S.step>=3,sarcomere_length_percent:S.step>=3?88:100,filament_lengths_constant:true,scientific_interpretation:texteEtape()[1]},objective_progress:S.completed.size/4,timestamp:Date.now()},'*')}
function advance(){S.step++;const last=!S.calcium?1:!S.atp?2:5;if(S.step>=last){S.step=last;S.status='finished';S.completed.add(variant());stop();action('finish');bulle($('feedback'),S.calcium&&S.atp?'Les filaments ont glissé : les stries Z se sont rapprochées, chaque filament garde sa longueur.':'Essai terminé : compare avec les autres conditions.',S.calcium&&S.atp?'good':'')}else S.status='running';render();emit()}
function next(){stop();if(S.status==='finished')S.step=0;action('next');advance()}
function start(){stop();S.step=0;S.status='running';action('start');render();emit();bulle($('feedback'),'Observe les têtes de myosine et la distance Z–Z.');const tick=()=>{advance();if(S.status==='running')S.timer=setTimeout(tick,1800)};S.timer=setTimeout(tick,400)}
function setParameters(p){stop();if(typeof p.calcium_present==='boolean')S.calcium=p.calcium_present;if(typeof p.atp_present==='boolean')S.atp=p.atp_present;S.step=0;S.status='idle';action('set_parameters');render();bulle($('feedback'),`Condition : ${CONFIG.variants.find(v=>v.id===variant()).label}. Lance l’essai.`);emit()}
function setVariant(id){const choices={ca_atp:[true,true],sans_ca:[false,true],sans_atp:[true,false],sans_ca_atp:[false,false]};if(choices[id])setParameters({calcium_present:choices[id][0],atp_present:choices[id][1]})}
function reset(){stop();S.calcium=true;S.atp=true;S.step=0;S.status='idle';S.completed.clear();S.actions=[];S.ouvert=performance.now();S.marques={};action('reset');render();bulle($('feedback'),'Conditions initiales : Ca²⁺ et ATP disponibles.');emit()}
$('calcium').onchange=e=>setParameters({calcium_present:e.target.checked});$('atp').onchange=e=>setParameters({atp_present:e.target.checked});$('run').onclick=start;$('next').onclick=next;$('reset').onclick=reset;
window.executeAICommand=(command,p={})=>{if(command==='highlight'){window.Tableau.surligner(p.target||p.repere||p.id);return}appuyer(command);if(command==='start'||command==='replay')start();else if(command==='next')next();else if(command==='reset')reset();else if(command==='set_variant')setVariant(p.variant_id||p.variant);else if(command==='set_parameters')setParameters(p)};
window.addEventListener('message',e=>{const d=e.data||{};if(d.type==='simulation_control'&&(!d.simulation_id||d.simulation_id===CONFIG.id))window.executeAICommand(d.command,d.parameters||{})});

// ── Dessin à la craie (repère logique 900 × 350) ────────────────────────────
const craie=new Craie($('scene'),{onresize:()=>{S.dirty=true}});
const ease=k=>k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
function draw(){
 const W=craie.W,H=craie.H;if(W<1||H<1)return true;
 const temps=(performance.now()-S.ouvert)/1000;
 craie.debut(13,temps);
 const c=craie.ctx,s=Math.min(W/900,H/350);c.translate((W-900*s)/2,(H-350*s)/2);c.scale(s,s);craie.echelle=s;craie.tailleMin=11;
 const k=ease(Math.min(1,(performance.now()-S.t0)/700));S.shift=S.shiftFrom+(S.shiftTo-S.shiftFrom)*k;const sh=S.shift;
 // Repères fixes (sarcomère entre y = 95 et 310, cote en dessous)
 craie.ligne(450,80,450,300,{couleur:'tresfaible',largeur:1.2,pointille:[4,6],duree:.2}).texte('centre du sarcomère',462,62,{couleur:'faible',taille:14});
 craie.texte('━ actine (fine)',400,32,{couleur:'rose',taille:14}).texte('━ myosine (épaisse)',530,32,{couleur:'bleu',taille:14}).texte('┃ stries Z : limites',690,32,{couleur:'blanc',taille:14});
 craie.pause(.1);
 craie.ligne(270,190,630,190,{couleur:'bleu',largeur:16,alpha:.85});
 craie.texte('myosine',450,177,{couleur:'bleu',taille:13,align:'center'});
 craie.repere('myosine',266,176,368,30,'filament de myosine').repere('tetes_myosine',322,132,256,116,'têtes de myosine').repere('centre',440,50,210,40,'centre du sarcomère');
 // Parties mobiles : stries Z, actine, têtes, tropomyosine, cote Z–Z
 craie.direct(()=>{
  for(const [side,sign] of [['g',1],['d',-1]]){
   const zx=side==='g'?110+sh:790-sh;
   craie.ligne(zx,95,zx,285,{couleur:'blanc',largeur:6});craie.texte('Z',zx,308,{taille:17,align:'center'});
   craie.repere(side==='g'?'strie_z_gauche':'strie_z_droite',zx-14,90,28,230,side==='g'?'strie Z gauche':'strie Z droite');
   const ax=side==='g'?[zx,400+sh]:[zx,500-sh];
   craie.ligne(ax[0],140,ax[1],140,{couleur:'rose',largeur:9});craie.ligne(ax[0],240,ax[1],240,{couleur:'rose',largeur:9});
   if(side==='g'){craie.repere('actine',ax[0]+10,128,ax[1]-ax[0]-10,124,'filaments d’actine');craie.repere('stries_z',zx-14,90,790-sh-zx+28,230,'les deux stries Z');craie.repere('tropomyosine',276+sh,118,124,24,'tropomyosine')}
   if(!(S.calcium&&S.step>=1)){ // tropomyosine masque les sites
    const mx=side==='g'?[280+sh,395+sh]:[505-sh,620-sh];
    craie.ligne(mx[0],130,mx[1],130,{couleur:'jaune',largeur:4,pointille:[12,9]});craie.ligne(mx[0],250,mx[1],250,{couleur:'jaune',largeur:4,pointille:[12,9]});
   }
  }
  const col=S.step===2||S.step===3?'jaune':'bleu';
  const base=S.step===3?[[330,190,375,140],[385,190,410,240],[515,190,490,140],[570,190,525,240]]:S.step===2?[[330,190,350,140],[385,190,365,240],[515,190,535,140],[570,190,550,240]]:[[330,190,350,152],[385,190,365,228],[515,190,535,152],[570,190,550,228]];
  base.forEach(h=>craie.ligne(...h,{couleur:col,largeur:7}));
  let note=null,nc='jaune';
  if(!S.calcium&&S.step>=1){note='sites masqués par la tropomyosine';nc='rouge'}
  else if(S.step===2)note=S.atp?'ponts actine–myosine':'pont fixé : sans ATP il ne se détache pas';
  else if(S.step===3)note='coup de force : Pi puis ADP libérés';
  else if(S.step===4){note='ATP fixé : la tête se détache';nc='cyan'}
  else if(S.step===5){note='ATP + H₂O → ADP + Pi : tête réarmée';nc='vert'}
  if(note)craie.texte(note,450,275,{couleur:nc,taille:14,align:'center'});
  craie.cote(110+sh,328,790-sh,328,`distance Z–Z : ${Math.round((680-2*sh)/680*100)} % de la longueur initiale`,{couleur:'faible',largeur:1.6,taille:15,dessous:true});
  craie.repere('cote_zz',110+sh,318,680-2*sh,40,'distance Z–Z');if(note)craie.repere('note',290,258,320,24,'ce qui se passe');
 });
 const complet=craie.fin();
 return complet&&k>=1;
}
function frame(){if(S.dirty||S.status==='running')S.dirty=!draw();requestAnimationFrame(frame)}
ecrire($('objectif'),'Change une condition, observe, puis explique. Modèle : têtes déjà armées au départ ; sans ATP, un pont formé reste fixé.',{vitesse:70});
render();bulle($('feedback'),'Avec Ca²⁺ et ATP, les cycles peuvent se répéter. Et sans l’un des deux ?');requestAnimationFrame(frame);
window.__SIMULATION_MANIFEST_SENT__=true;
// Les repères pointables sont connus après le premier dessin : le manifeste est renvoyé une fois complet.
function manifeste(){window.parent.postMessage({type:'simulation_manifest',simulation_id:CONFIG.id,capabilities:{commands:CONFIG.commands,config:CONFIG,controls:{calcium_present:{type:'boolean'},atp_present:{type:'boolean'}},command_schema:{highlight:{target:Object.keys(window.Tableau.listeReperes()).join(' | ')}},state_schema:{cycle_step:'0..5',sarcomere_shortening:'boolean',scientific_interpretation:'conclusion'},reperes:window.Tableau.listeReperes(),explication:EXPLICATION},page_text:'Sarcomère dessiné au tableau : comparer quatre conditions Ca²⁺ / ATP, avancer pas à pas et observer les stries Z sans raccourcir les filaments.'},'*')}
manifeste();setTimeout(manifeste,1800);emit();
