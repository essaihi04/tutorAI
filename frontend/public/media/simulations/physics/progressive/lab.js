import { pulse, speed, springPosition, arrivals, assess } from './model.js';

const $ = id => document.getElementById(id);
const variants = {
  cord: ['Corde', 'Un point reste près de sa place', 'Suis le point orange pendant le passage de l’impulsion.', 'Le déplacement du point orange est…', ['Perpendiculaire à la propagation', 'Parallèle à la propagation', 'Un voyage jusqu’au bout de la corde'], 0, 'Compare la flèche horizontale et le mouvement du point.'],
  spring: ['Ressort', 'Une compression de proche en proche', 'Suis une spire repérée et compare les directions.', 'Le mouvement local des spires est…', ['Parallèle à la propagation', 'Perpendiculaire à la propagation', 'Un transport de tout le ressort'], 0, 'Observe la spire orange et sa position d’équilibre.'],
  water: ['Surface de l’eau', 'Une perturbation dans un plan', 'Lance une perturbation au centre et observe le front circulaire.', 'Dans ce modèle, les rides se propagent…', ['Dans le plan de la surface : 2D', 'Sur une seule droite : 1D', 'Dans tout le volume de l’eau : 3D'], 0, 'La vue montre le dessus de la surface.'],
  sound: ['Son dans l’air', 'L’air vibre localement', 'Observe la membrane, les compressions et un point matériel orange.', 'Dans l’air, le son est une onde…', ['Longitudinale', 'Transversale', 'Qui transporte les molécules jusqu’à l’oreille'], 0, 'Les points oscillent horizontalement autour de leurs positions de repos.'],
  vacuum: ['Cloche à vide', 'Quel rôle joue le milieu ?', 'Compare deux quantités d’air. La source continue à vibrer.', 'Quand on retire presque tout l’air, la transmission sonore par l’air…', ['Diminue alors que la source peut encore vibrer', 'Augmente', 'Ne dépend pas de l’air'], 0, 'Compare le mouvement de la source et la jauge de transmission.'],
  superposition: ['Superposition', 'Avant, pendant, après', 'Essaie les deux signes. À t = 2,5 s les centres coïncident.', 'Après leur rencontre, deux petites impulsions idéales…', ['Poursuivent leur propagation', 'Disparaissent définitivement', 'Restent bloquées au centre'], 0, 'Arrête à 2,5 s, puis observe à 4 s.'],
  medium: ['Influence du milieu', 'Qu’est-ce qui change la célérité ?', 'Compare tension et masse linéique, puis change seulement l’amplitude.', 'À tension et masse linéique fixées, augmenter une petite amplitude…', ['Ne change pas la célérité du modèle', 'Double toujours la célérité', 'Arrête la propagation'], 0, 'Dans ce modèle linéaire : v = √(T/μ).'],
  progressive: ['Capteurs et retard', 'Mesurer puis calculer', 'Lis les dates des maxima, calcule τ et v, puis compare deux distances.', 'Calcule à partir de tes lectures.', [], 0, 'τ = tB − tA ; v = AB/τ. Les axes sont en secondes et mètres.'],
};
const id = 'physics_waves_advanced_lab';
const requested = new URLSearchParams(location.search).get('variant');
const initial = variants[requested] ? requested : 'cord';
const focusOnly = new URLSearchParams(location.search).get('scope') === 'single';
const S = { variant: initial, time: 0, running: false, observed: false, status: 'idle', completed: new Set(), actions: [], measurements: [], visits: {}, attempts: 0, hints: 0, validated: false, trial: null, stopAt: null,
  params: { speed: 4, sensor1: 2, sensor2: 7, amplitude: 1, tension: 4, density: .25, air: 100, sign: -1 } };
const numericLimits = {speed:[1,10],sensor1:[1,5],sensor2:[5.5,9],amplitude:[.3,1.5],tension:[1,9],density:[.1,.5],air:[0,100],sign:[-1,1]};
const commandMap = {speed_m_s:'speed',sensor_1_m:'sensor1',sensor_2_m:'sensor2',mass_density_kg_m:'density',tension_n:'tension'};
function log(action, details = {}) { S.actions.push({action, details, variant:S.variant, timestamp:Date.now()}); S.actions = S.actions.slice(-80); }
function ratio() { return focusOnly ? Number(S.completed.has(S.variant)) : S.completed.size / Object.keys(variants).length; }
function snapshot() { return {simulation_status:S.status, current_variant:S.variant, time_s:+S.time.toFixed(2), duration_s:+duration().toFixed(2), parameters:{...S.params}, acquisition_complete:acquired(), student_observed:S.observed, attempts:S.attempts, hints_used:S.hints, completed_variants:[...S.completed], measurements:S.measurements, student_response:readAnswer(), objective_progress:ratio()}; }
function emit(extra = {}) { parent.postMessage({type:'simulation_state', simulation_id:id, current_state:{...snapshot(),...extra},student_actions:S.actions,objective_progress:ratio(),timestamp:Date.now()},'*'); $('progress').textContent = focusOnly ? (ratio() ? 'Objectif validé' : 'Objectif en cours') : `${S.completed.size} / 8 expériences`; }
const commands = ['start','set_variant','set_parameters','fire_pulse','pause','step','run_until','set_time','record_measurement','check','reset','reveal_hint'];
window.SIMULATION_CONFIG = {id, version:'3.0', title:'Ondes mécaniques progressives',variants:Object.entries(variants).map(([id,v])=>({id,label:v[0],objective:v[2]})),commands,command_schema:{set_variant:{variant_id:Object.keys(variants).join(' | ')},run_until:{time_s:'0..duration_s (lance si besoin, puis s’arrête à cet instant)'},set_time:{time_s:'0..duration_s (saute à cet instant, en pause)'},set_parameters:{speed_m_s:'1..10',sensor_1_m:'1..5',sensor_2_m:'5.5..9',amplitude:'.3..1.5',tension_n:'1..9',mass_density_kg_m:'.1...5',air:'0..100',sign:'-1 | 1'}}};
function manifest() { parent.postMessage({type:'simulation_manifest',simulation_id:id,capabilities:{commands,config:window.SIMULATION_CONFIG,globals:['executeAICommand'],command_schema:window.SIMULATION_CONFIG.command_schema},page_text:'Huit expériences : corde, ressort, eau, son, cloche, superposition, milieu et retard. Les réponses sont saisies par l’élève ; deux calculs validés à distances différentes terminent la mesure.'},'*'); }
function feedback(text, error = false) { $('feedback').textContent = text; $('feedback').dataset.error = String(error); }
function tab(answer) { $('settings').hidden = answer; $('answers').hidden = !answer; $('settingsTab').setAttribute('aria-pressed',String(!answer)); $('answerTab').setAttribute('aria-pressed',String(answer)); }
function range(key, label, min, max, step, unit) { const el = document.createElement('label'); el.className='control'; el.innerHTML=`<span>${label}<b>${S.params[key]} ${unit}</b></span><input aria-label="${label}" type="range" min="${min}" max="${max}" step="${step}" value="${S.params[key]}">`; el.querySelector('input').addEventListener('change',e=>setParameters({[key]:Number(e.target.value)})); $('controls').append(el); }
function controls() {
  $('controls').replaceChildren();
  if (S.variant==='progressive') { range('sensor1','Capteur A',1,5,.5,'m'); range('sensor2','Capteur B',5.5,9,.5,'m'); const p=document.createElement('p'); p.className='help'; p.textContent='Même milieu pour les deux essais. La célérité est à déterminer.'; $('controls').append(p); }
  else if (S.variant==='medium') { range('tension','Tension T',1,9,1,'N'); range('density','Masse linéique μ',.1,.5,.05,'kg/m'); range('amplitude','Amplitude relative',.3,1.5,.1,''); }
  else if (S.variant==='vacuum') range('air','Air restant',0,100,10,'%');
  else if (S.variant==='superposition') { const el=document.createElement('label');el.className='control';el.textContent='Deuxième impulsion';const select=document.createElement('select');select.innerHTML='<option value="-1">Signe opposé</option><option value="1">Même signe</option>';select.value=String(S.params.sign);select.onchange=e=>setParameters({sign:Number(e.target.value)});el.append(select);$('controls').append(el); }
  else range('amplitude','Amplitude relative',.3,1.5,.1,'');
}
function responses() {
  $('question').textContent=variants[S.variant][3]; $('response').replaceChildren();
  if (S.variant==='progressive') { $('response').innerHTML='<label>Retard τ (s)<input id="delayAnswer" type="text" inputmode="decimal" autocomplete="off"></label><label>Célérité v (m/s)<input id="speedAnswer" type="text" inputmode="decimal" autocomplete="off"></label>'; }
  else {const options=variants[S.variant][4]; const offset=Object.keys(variants).indexOf(S.variant)%options.length; options.map((_,i)=>(i+offset)%options.length).forEach(i=>{const label=document.createElement('label');const input=document.createElement('input');input.type='radio';input.name='choice';input.value=String(i);label.append(input,document.createTextNode(' '+options[i]));$('response').append(label);});}
  $('response').oninput=()=>{S.validated=false;$('record').disabled=true;};
  $('record').hidden=S.variant!=='progressive'; $('record').disabled=true; updateHistory();
}
function updateHistory() { $('history').textContent=S.variant==='progressive'?S.measurements.slice(-2).map(m=>`AB ${m.distance_m} m : τ ${m.student_delay_s} s ; v ${m.student_speed_m_s} m/s`).join(' · '):''; }
function reset() { S.running=false; S.stopAt=null; S.time=0; S.observed=false; S.validated=false; S.trial=null; S.status='idle'; $('record').disabled=true; $('pause').textContent='Pause'; log('reset');feedback('Nouvel essai. Lance puis observe la perturbation.');draw();emit(); }
function setVariant(variant) { if (!variants[variant]) return; S.variant=variant; $('variant').value=variant; $('eyebrow').textContent=variants[variant][0].toUpperCase();$('title').textContent=variants[variant][1];$('objective').textContent=variants[variant][2]; controls();responses();tab(false);reset();log('set_variant',{variant_id:variant});emit(); }
function setParameters(values) { let changed=false; for (const [raw,value] of Object.entries(values||{})) { const key=commandMap[raw]||raw;const bounds=numericLimits[key]; if (!bounds||!Number.isFinite(Number(value))) continue; const v=Math.min(bounds[1],Math.max(bounds[0],Number(value))); if(key==='sign' && v!==-1 && v!==1) continue; if(S.params[key]!==v) {S.params[key]=v;changed=true;} } if(changed){reset();controls();log('set_parameters',{...S.params});emit();} }
function duration() { return S.variant==='progressive'? (10.7/S.params.speed) : S.variant==='medium'? 10.7/speed(S.params.tension,S.params.density) : 5; }
function acquired() { return S.variant==='progressive' && !!S.trial && S.time >= (S.trial.sensor2+.65)/S.trial.speed; }
function observe() { if (S.time < Math.min(S.variant==='superposition'?4:.4,duration())) return; S.observed=true; const key=S.variant==='vacuum' ? S.params.air : S.variant==='medium' ? `${S.params.tension}/${S.params.density}/${S.params.amplitude}` : S.variant==='superposition'?S.params.sign:'seen'; (S.visits[S.variant]??=new Set()).add(key); }
function launch() { S.time=0;S.stopAt=null;S.running=true;S.observed=false;S.validated=false;S.trial={...S.params};S.status='running';$('record').disabled=true;$('pause').textContent='Pause';log('fire_pulse',{...S.trial});feedback('Observation en cours. Tu peux mettre en pause et avancer pas à pas.');emit(); }
function pause() { if(!S.trial) return;S.running=!S.running;if(S.time>=duration()) S.running=false;if(S.status!=='finished') S.status=S.running?'running':'paused';$('pause').textContent=S.running?'Pause':'Reprendre';log('pause');emit(); }
function step() { if(!S.trial) { S.trial={...S.params}; } S.running=false;S.time=Math.min(duration(),S.time+.1);if(S.status!=='finished') S.status='paused';observe();$('pause').textContent='Reprendre';draw();log('step');emit(); }
function clampTime(t) { return Math.min(duration(),Math.max(0,Number(t)||0)); }
// Le tuteur arrête la scène à un instant précis : « observe à t = 2,5 s ».
function setTime(t) { const target=clampTime(t); if(!S.trial) S.trial={...S.params}; S.running=false;S.stopAt=null;S.time=target;if(S.status!=='finished') S.status='paused';observe();$('pause').textContent='Reprendre';draw();log('set_time',{time_s:target});feedback(`Arrêt à t = ${target.toFixed(2)} s. Observe, puis reprends ou avance pas à pas.`);emit(); }
function runUntil(t) { const target=clampTime(t); if(!S.trial||S.time>=target) launch(); S.stopAt=target;S.running=true;S.status='running';$('pause').textContent='Pause';log('run_until',{time_s:target});emit(); }
function number(id) { const raw=$(id)?.value?.trim(); return raw ? Number(raw.replace(',','.')) : NaN; }
function readAnswer() { if(S.variant==='progressive') return {delay_s:Number.isFinite(number('delayAnswer'))?number('delayAnswer'):null,speed_m_s:Number.isFinite(number('speedAnswer'))?number('speedAnswer'):null};return {choice:document.querySelector('input[name=choice]:checked')?.value??null}; }
function complete() { S.completed.add(S.variant);S.status='finished';feedback('Objectif validé. Explique maintenant ton observation au tuteur.');emit({correct:true}); }
function check() {
  S.attempts++;log('check',{answer:readAnswer()});
  if(!S.observed) {feedback('Lance et observe l’expérience avant de répondre.',true);emit({correct:false});return;}
  if(S.variant==='progressive') {const result=assess(S.trial,S.time,{delay:number('delayAnswer'),speed:number('speedAnswer')}); S.validated=result.correct;$('record').disabled=!result.correct;feedback(result.reason,!result.correct);emit({correct:result.correct});return;}
  const visits=S.visits[S.variant];
  if(S.variant==='vacuum' && !(visits?.has(100)&&visits?.has(0))) {feedback('Compare une observation à 100 % d’air et une à 0 %.',true);emit({correct:false});return;}
  if(S.variant==='superposition' && !(visits?.has(-1)&&visits?.has(1))) {feedback('Observe les deux cas : même signe et signe opposé.',true);emit({correct:false});return;}
  if(S.variant==='medium') {
    const trials=[...(visits||[])].map(x=>x.split('/').map(Number));
    const amplitudeOnly=trials.some(a=>trials.some(b=>a[0]===b[0]&&a[1]===b[1]&&a[2]!==b[2]));
    const mediumOnly=trials.some(a=>trials.some(b=>a[2]===b[2]&&((a[0]!==b[0]&&a[1]===b[1])||(a[0]===b[0]&&a[1]!==b[1]))));
    if(!amplitudeOnly||!mediumOnly){feedback('Compare le milieu en gardant l’amplitude fixe, puis change seulement l’amplitude.',true);emit({correct:false});return;}
  }
  const correct=Number(readAnswer().choice)===variants[S.variant][5] && readAnswer().choice!==null;
  if(correct) complete(); else {feedback('Réessaie en comparant les mouvements et les directions.',true);emit({correct:false});}
}
function recordMeasurement() {
  if(!S.validated||!acquired()) {feedback('Termine l’acquisition et vérifie ton calcul avant de l’enregistrer.',true);return;}
  const result=assess(S.trial,S.time,{delay:number('delayAnswer'),speed:number('speedAnswer')});if(!result.correct)return;
  const a=arrivals(S.trial);const item={distance_m:a.distance,arrival_1_s:a.a,arrival_2_s:a.b,student_delay_s:number('delayAnswer'),student_speed_m_s:number('speedAnswer'),parameters:{...S.trial}};
  S.measurements.push(item);S.measurements=S.measurements.slice(-12);S.validated=false;$('record').disabled=true;log('record_measurement',item);updateHistory();
  const match=S.measurements.some(m=>m.distance_m!==item.distance_m&&m.parameters.speed===item.parameters.speed);
  if(match)complete();else {feedback('Essai enregistré. Déplace B, recommence et compare.');emit();}
}
function hint() {S.hints++;feedback(variants[S.variant][6]);log('reveal_hint');emit();}

const canvas=$('canvas'),ctx=canvas.getContext('2d');
const ink='#24473f',teal='#187763',orange='#bd641c',blue='#366dc1';
let drawScale=1;
function line(x1,y1,x2,y2,color=ink,width=2) {ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();}
function text(s,x,y,color=ink,size=14) {if(drawScale<.3)return;ctx.fillStyle=color;ctx.font=`${Math.max(size,10/drawScale)}px system-ui`;ctx.fillText(s,x,y);}
function dot(x,y,r,color) {ctx.fillStyle=color;ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();}
function arrow(x1,y1,x2,y2,color=teal) {line(x1,y1,x2,y2,color);const a=Math.atan2(y2-y1,x2-x1);line(x2,y2,x2-9*Math.cos(a-.5),y2-9*Math.sin(a-.5),color);line(x2,y2,x2-9*Math.cos(a+.5),y2-9*Math.sin(a+.5),color);}
function curve(fn,left,right,y,scale,color=teal) {ctx.beginPath();for(let i=0;i<=200;i++){const x=i/200*10;const yy=y-fn(x)*scale; i?ctx.lineTo(left+(right-left)*i/200,yy):ctx.moveTo(left,yy);}ctx.strokeStyle=color;ctx.lineWidth=2.5;ctx.stroke();}
function resize() {const r=canvas.getBoundingClientRect(); const d=devicePixelRatio||1;canvas.width=Math.max(1,r.width*d);canvas.height=Math.max(1,r.height*d);draw();}
function draw() {
  const W=canvas.clientWidth,H=canvas.clientHeight;if(W<1||H<1)return;ctx.setTransform(devicePixelRatio||1,0,0,devicePixelRatio||1,0,0);ctx.clearRect(0,0,W,H);
  // Logical coordinates keep labels and apparatus aligned across viewport sizes.
  const scale=Math.min(W/760,H/360);drawScale=scale;ctx.translate((W-760*scale)/2,(H-360*scale)/2);ctx.scale(scale,scale);
  const p=S.params,t=S.time,left=45,right=710,y=175,amp=38*p.amplitude;let description='';$('readings').textContent='';
  if(['cord','medium','progressive'].includes(S.variant)) {
    const v=S.variant==='medium'?speed(p.tension,p.density):p.speed;const center=v*t;
    const yy=S.variant==='progressive'?85:y;line(left,yy,right,yy,'#b8cac2',1);curve(x=>pulse(x,center),left,right,yy,amp);
    const px=4;dot(left+(right-left)*px/10,yy-pulse(px,center)*amp,6,orange);line(left+(right-left)*px/10,yy+25,left+(right-left)*px/10,yy-65,orange,1);
    arrow(70,yy-65,220,yy-65);text('propagation →',80,yy-80);text('S',left-20,yy+5);
    if(S.variant==='progressive') {
      const a=arrivals(p);$('readings').textContent=`AB = ${a.distance.toFixed(2)} m · tA = ${t>=a.a?a.a.toFixed(3)+' s':'…'} · tB = ${t>=a.b?a.b.toFixed(3)+' s':'…'}`;[p.sensor1,p.sensor2].forEach((x,i)=>{const sx=left+(right-left)*x/10;line(sx,yy-20,sx,yy+30,blue);text(i?'B':'A',sx-4,yy+46,blue);});text(`AB = ${a.distance.toFixed(2)} m`,500,30);
      const total=10.7/p.speed,gx=85,gw=590;
      [a.a,a.b].forEach((arrival,i)=>{const gy=200+i*95;line(gx,gy,gx+gw,gy,'#b8cac2');text(i?'yB':'yA',40,gy,blue);ctx.beginPath();for(let j=0;j<=200;j++){const tt=j/200*total;const val=tt<=t?pulse(p.speed*tt,p.speed*arrival):0;const xx=gx+j/200*gw,yy=gy-val*43;j?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy);}ctx.strokeStyle=i?orange:blue;ctx.stroke();if(t>=arrival){text(`${i?'tB':'tA'} = ${arrival.toFixed(3)} s`,gx+(arrival/total)*gw-35,gy-52,i?orange:blue);}for(let j=0;j<=4;j++){const x=gx+j/4*gw;line(x,gy,x,gy+4);text((j*total/4).toFixed(2),x-12,gy+21,ink,12);}text('t (s)',685,gy+5);});
      description='Lecture des maxima : les courbes représentent le déplacement aux capteurs, en unités arbitraires. AB est une distance en mètres.';
    } else {text('point matériel repéré',270,280,orange);text('position x (m)',580,215); for(let i=0;i<=10;i+=2)text(String(i),left+i/10*(right-left),200); description=S.variant==='medium'?`Corde idéale : v = √(T/μ) = ${v.toFixed(2)} m/s. L’amplitude ne modifie pas v dans ce modèle.`:'Le point orange monte puis redescend à la même abscisse ; la perturbation avance.';}
  } else if(S.variant==='spring'||S.variant==='sound') {
    const sound=S.variant==='sound';const shift=x=>sound ? .2*p.amplitude*Math.sin(2*Math.PI*(x/2-t)) : springPosition(x,2*t,p.amplitude)-x;
    for(let row=0;row<(sound?4:1);row++)for(let i=0;i<=75;i++){const x=i/75*10,xx=left+(x+shift(x))/10*(right-left),yy=sound?125+row*30:y; if(sound)dot(xx,yy,3,i===30?orange:blue);else line(xx,yy-36,xx,yy+36,i===30?orange:blue,2);}
    arrow(85,55,235,55);text('propagation',100,40);arrow(310,280,360,280,orange);arrow(360,300,310,300,orange);text('mouvement local ↔',275,330,orange);text(sound?'membrane':'spires',15,100);if(sound)line(32+8*Math.sin(2*Math.PI*t),110,32+8*Math.sin(2*Math.PI*t),230,ink,6);
    description='Les éléments orange oscillent autour d’une position fixe. Les zones resserrées sont des compressions ; les zones espacées, des dilatations.';
  } else if(S.variant==='water') {
    const cx=350,cy=170;for(let r=0;r<4;r++){const radius=70*t-r*28;if(radius>0&&radius<165){ctx.strokeStyle=teal;ctx.lineWidth=3;ctx.beginPath();ctx.arc(cx,cy,radius,0,Math.PI*2);ctx.stroke();}}dot(cx,cy,6,blue);text('S · impact',cx+12,cy+5);arrow(350,170,500,170);arrow(350,170,350,50);text('Surface vue du dessus',245,345);description='Les fronts s’étendent dans le plan de la surface. Le dessin représente la propagation, pas la trajectoire des particules d’eau.';
  } else if(S.variant==='vacuum') {
    ctx.strokeStyle=blue;ctx.lineWidth=3;ctx.beginPath();ctx.roundRect(160,30,280,260,[130,130,0,0]);ctx.stroke();line(140,294,460,294,ink,7);
    for(let i=0;i<Math.round(p.air*.6);i++){const x=185+(i*47%230),y=100+(i*31%170);dot(x,y,2,teal);}const wiggle=Math.sin(t*15)*4;ctx.strokeRect(265+wiggle,175,68,65);text('source vibrante',230,325);text('Transmission par l’air',480,130);ctx.strokeStyle='#b8cac2';ctx.strokeRect(485,150,190,25);ctx.fillStyle=teal;ctx.fillRect(485,150,190*p.air/100,25);text(p.air===0?'nulle dans ce modèle':p.air<50?'affaiblie':'présente',485,205);text(`${p.air} % d’air (réglage)`,480,245);description='Modèle qualitatif, sans son joué : la jauge n’est pas une mesure en décibels. Une expérience réelle peut transmettre un son résiduel par les supports.';
  } else if(S.variant==='superposition') {
    const a=x=>pulse(x,2*t,.85),b=x=>pulse(x,10-2*t,.85*p.sign);curve(a,left,right,80,38,blue);curve(b,left,right,165,38,orange);curve(x=>a(x)+b(x),left,right,270,38,teal);text('impulsion 1 →',50,30,blue);text('← impulsion 2',50,125,orange);text('somme des déplacements',50,218,teal);description='Somme algébrique des deux perturbations. Au croisement exact : double amplitude pour deux impulsions identiques, déplacement nul pour deux opposées.';
  }
  $('description').textContent=description;canvas.setAttribute('aria-label',description);$('clock').textContent=`t = ${t.toFixed(2)} s`;
}
$('variant').innerHTML=Object.entries(variants).map(([key,v])=>`<option value="${key}">${v[0]}</option>`).join('');
$('variant').onchange=e=>setVariant(e.target.value);$('settingsTab').onclick=()=>tab(false);$('answerTab').onclick=()=>tab(true);$('run').onclick=launch;$('pause').onclick=pause;$('step').onclick=step;$('reset').onclick=reset;$('check').onclick=check;$('record').onclick=recordMeasurement;$('hint').onclick=hint;
$('zoom').onclick=()=>{const zoom=document.body.classList.toggle('zoom');$('zoom').textContent=zoom?'Réduire':'Agrandir';$('zoom').setAttribute('aria-pressed',String(zoom));};
window.executeAICommand=(command,p={})=>{if(command==='set_variant')setVariant(p.variant_id);else if(command==='set_parameters'){tab(false);setParameters(p);}else if(command==='start'||command==='fire_pulse')launch();else if(command==='pause')pause();else if(command==='step')step();else if(command==='run_until')runUntil(p.time_s??p.time);else if(command==='set_time')setTime(p.time_s??p.time);else if(command==='reset')reset();else if(command==='check')check();else if(command==='record_measurement')recordMeasurement();else if(command==='reveal_hint')hint();};
// La localisation des boutons pour le professeur (`simulation_locate`) est assurée par ../../professor-locate.js.
addEventListener('message',e=>{if(e.source!==parent)return;const d=e.data;if(d?.type==='simulation_control'&&(!d.simulation_id||d.simulation_id===id)&&commands.includes(d.command))window.executeAICommand(d.command,d.parameters||{});});
let previous=performance.now(),lastEmit=0;
function frame(now) {const dt=Math.min(.1,(now-previous)/1000);previous=now;if(S.running){S.time=Math.min(duration(),S.time+dt);observe();if(S.stopAt!==null&&S.time>=S.stopAt){S.time=S.stopAt;S.stopAt=null;S.running=false;if(S.status!=='finished') S.status='paused';$('pause').textContent='Reprendre';feedback(`Arrêt à t = ${S.time.toFixed(2)} s. Observe, puis reprends ou avance pas à pas.`);emit();}else if(S.time>=duration()){S.running=false;feedback('Observation terminée. Ouvre « Répondre » pour interpréter.');emit();}draw();if(S.running&&now-lastEmit>500){lastEmit=now;emit();}}requestAnimationFrame(frame);}
new ResizeObserver(resize).observe(canvas);setVariant(initial);manifest();setTimeout(manifest,350);requestAnimationFrame(frame);
