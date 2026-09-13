'use strict';
const CONFIG={id:'svt_ch1_contraction_actine_myosine',variants:[{id:'ca_atp',label:'Ca²⁺ et ATP'},{id:'sans_ca',label:'Sans Ca²⁺'},{id:'sans_atp',label:'Sans ATP'},{id:'sans_ca_atp',label:'Sans Ca²⁺ ni ATP'}],objectives:['Distinguer les rôles de Ca²⁺ et ATP et observer le glissement à longueur de filament constante.'],commands:['start','set_variant','set_parameters','reset','replay','next']};
window.SIMULATION_CONFIG=CONFIG;
const S={calcium:true,atp:true,status:'idle',step:0,completed:new Set(),actions:[],timer:null};
const $=id=>document.getElementById(id);
const steps=[['Prédis le résultat','Avec Ca²⁺ et ATP, les cycles peuvent se répéter. Que se passe-t-il si tu retires l’un des deux ?'],['Le calcium autorise la liaison','Le Ca²⁺ se fixe à la troponine. La tropomyosine se déplace : les sites de l’actine deviennent accessibles.'],['La myosine s’accroche','Une tête déjà armée, portant ADP et Pi, se lie à un site accessible de l’actine.'],['La tête pivote et tire l’actine','La libération de Pi accompagne le coup de force, puis l’ADP est libéré. Les stries Z se rapprochent ; les filaments gardent leur longueur.'],['Un nouvel ATP détache la tête','La fixation d’un nouvel ATP sur la myosine rompt le pont avec l’actine. Fixation et hydrolyse sont deux étapes différentes.'],['L’hydrolyse réarme la tête','ATP + H₂O → ADP + Pi. L’énergie libérée réarme la myosine. Un autre cycle devient possible si le Ca²⁺ reste disponible.']];
function variant(){return S.calcium?(S.atp?'ca_atp':'sans_atp'):(S.atp?'sans_ca':'sans_ca_atp')}
function stop(){clearTimeout(S.timer);S.timer=null}
function action(name){S.actions.push({action:name,variant:variant(),step:S.step});S.actions=S.actions.slice(-24)}
function render(){
 $('calcium').checked=S.calcium;$('atp').checked=S.atp;
 const shift=S.step>=3?40:0;
 $('left').setAttribute('transform',`translate(${shift} 0)`);$('right').setAttribute('transform',`translate(${-shift} 0)`);
 $('measure').setAttribute('x1',110+shift);$('measure').setAttribute('x2',790-shift);
 $('length').textContent=`Distance Z–Z : ${Math.round((680-2*shift)/680*100)} % de la longueur initiale`;
 $('bands').textContent=shift?'diminuent':'au repos';
 $('masks').style.opacity=S.calcium&&S.step>=1?'0':'1';
 $('heads').setAttribute('stroke',S.step===2||S.step===3?'#fcd34d':'#7db9ff');
 $('heads').firstElementChild.setAttribute('d',S.step===3?'M330 165L375 115 M385 165L410 215 M515 165L490 115 M570 165L525 215':S.step===2?'M330 165L350 115 M385 165L365 215 M515 165L535 115 M570 165L550 215':'M330 165L350 127 M385 165L365 203 M515 165L535 127 M570 165L550 203');
 let [title,text]=steps[S.step];
 if(S.step>0&&!S.calcium){title='Sites masqués : aucun nouveau pont';text=S.atp?'Même avec ATP, l’absence de Ca²⁺ empêche l’accès aux sites de l’actine. Aucun glissement dans cet essai.':'Sans Ca²⁺, aucun nouveau pont ne se forme ici. Sans ATP, des ponts déjà fixés ne pourraient pas se détacher.'}
 else if(S.step===2&&!S.atp){title='Pont fixé : le cycle est bloqué';text='La tête était déjà armée au départ. Sans nouvel ATP, un pont formé ne peut pas se détacher. Ce modèle montre le blocage, pas une contraction répétée.'}
 $('title').textContent=title;$('text').textContent=text;$('step').textContent=S.step?`ÉTAPE ${S.step} / 5`:'AVANT L’ESSAI';
 $('status').textContent={idle:'Prêt',running:'Observation',finished:'Essai terminé'}[S.status];
 $('run').textContent=S.status==='finished'?'↻ Rejouer':'▶ Animer';
 $('coverage').textContent=`${S.completed.size} / 4 conditions observées`;
}
function emit(){window.parent.postMessage({type:'simulation_state',simulation_id:CONFIG.id,student_actions:S.actions,current_state:{simulation_status:S.status,current_variant:variant(),variants_completed:[...S.completed],calcium_present:S.calcium,atp_present:S.atp,cycle_step:S.step,sarcomere_shortening:S.step>=3,sarcomere_length_percent:S.step>=3?88:100,filament_lengths_constant:true,scientific_interpretation:$('text').textContent},objective_progress:S.completed.size/4,timestamp:Date.now()},'*')}
function advance(){S.step++;const last=!S.calcium?1:!S.atp?2:5;if(S.step>=last){S.step=last;S.status='finished';S.completed.add(variant());stop();action('finish')}else S.status='running';render();emit()}
function next(){stop();if(S.status==='finished')S.step=0;action('next');advance()}
function start(){stop();S.step=0;S.status='running';action('start');render();emit();const tick=()=>{advance();if(S.status==='running')S.timer=setTimeout(tick,1600)};S.timer=setTimeout(tick,350)}
function setParameters(p){stop();if(typeof p.calcium_present==='boolean')S.calcium=p.calcium_present;if(typeof p.atp_present==='boolean')S.atp=p.atp_present;S.step=0;S.status='idle';action('set_parameters');render();emit()}
function setVariant(id){const choices={ca_atp:[true,true],sans_ca:[false,true],sans_atp:[true,false],sans_ca_atp:[false,false]};if(choices[id])setParameters({calcium_present:choices[id][0],atp_present:choices[id][1]})}
function reset(){stop();S.calcium=true;S.atp=true;S.step=0;S.status='idle';S.completed.clear();S.actions=[];action('reset');render();emit()}
$('calcium').onchange=e=>setParameters({calcium_present:e.target.checked});$('atp').onchange=e=>setParameters({atp_present:e.target.checked});$('run').onclick=start;$('next').onclick=next;$('reset').onclick=reset;
window.executeAICommand=(command,p={})=>{if(command==='start'||command==='replay')start();else if(command==='next')next();else if(command==='reset')reset();else if(command==='set_variant')setVariant(p.variant_id||p.variant);else if(command==='set_parameters')setParameters(p)};
window.addEventListener('message',e=>{const d=e.data||{};if(d.type==='simulation_control'&&(!d.simulation_id||d.simulation_id===CONFIG.id))window.executeAICommand(d.command,d.parameters||{})});
render();window.__SIMULATION_MANIFEST_SENT__=true;window.parent.postMessage({type:'simulation_manifest',simulation_id:CONFIG.id,capabilities:{commands:CONFIG.commands,config:CONFIG,controls:{calcium_present:{type:'boolean'},atp_present:{type:'boolean'}},state_schema:{cycle_step:'0..5',sarcomere_shortening:'boolean',scientific_interpretation:'conclusion'}},page_text:'Comparer quatre conditions Ca²⁺ / ATP, avancer pas à pas et observer les stries Z sans raccourcir les filaments.'},'*');emit();
