import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
const output='tmp/muscle-course';
mkdirSync(output,{recursive:true});
import { createRequire } from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{channel:'msedge'})});
const base=process.env.TEST_BASE_URL || 'http://localhost:5173';
const path='/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html';
try {
 const page=await browser.newPage({viewport:{width:1100,height:720}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{window.states=[];window.addEventListener('message',e=>{if(e.data?.type==='simulation_state')window.states.push(e.data)})});
 await page.goto(base+path);
 const state=async()=>{await page.waitForTimeout(80);return page.evaluate(()=>window.states.at(-1))};
 const command=async(command,parameters={})=>{await page.evaluate(({command,parameters})=>window.postMessage({type:'simulation_control',simulation_id:'svt_ch1_contraction_actine_myosine',command,parameters},'*'),{command,parameters});await page.waitForTimeout(35)};
 const geometry=()=>page.evaluate(()=>{const l=document.querySelector('#left');return {path:l.querySelector('path').getAttribute('d'),z:l.querySelector('line').getAttribute('x1'),transform:l.getAttribute('transform')}});
 const before=await geometry();
 for(let i=0;i<3;i++)await page.locator('#next').click();
 const after=await geometry();assert.equal(after.path,before.path);assert.equal(after.z,before.z);assert.notEqual(after.transform,before.transform);
 assert.equal((await state()).current_state.sarcomere_shortening,true);
 for(let i=0;i<2;i++)await page.locator('#next').click();
 assert.equal((await state()).current_state.simulation_status,'finished');
 for(const [v,n] of [['sans_ca',1],['sans_atp',2],['sans_ca_atp',1]]){
  await command('set_variant',{variant_id:v});
  for(let i=0;i<n;i++)await page.locator('#next').click();
  const s=await state();assert.equal(s.current_state.current_variant,v);assert.equal(s.current_state.simulation_status,'finished');assert.equal(s.current_state.sarcomere_shortening,false);
 }
 assert.equal((await state()).objective_progress,1);
 await command('reset');assert.equal((await state()).objective_progress,0);
 await command('set_variant',{variant_id:'sans_atp'});await command('start');await page.waitForTimeout(450);await command('reset');await page.waitForTimeout(2000);
 assert.equal((await state()).current_state.simulation_status,'idle');assert.equal((await state()).objective_progress,0);
 await command('start');await command('set_parameters',{calcium_present:false});await page.waitForTimeout(600);assert.equal((await state()).current_state.simulation_status,'idle');
 await command('set_variant',{variant_id:'ca_atp'});await command('replay');await page.waitForFunction(()=>window.states.at(-1)?.current_state.simulation_status==='finished');
 assert.equal((await state()).current_state.cycle_step,5);
 await page.screenshot({path:output+'/muscle-desktop.png'});
 for(const [width,height] of [[550,530],[390,700],[900,500]]){
  await page.setViewportSize({width,height});
  if(width===550)await page.screenshot({path:output+'/muscle-compact.png'});
  const clipped=await page.evaluate(()=>[...document.querySelectorAll('button,.explanation,footer')].some(e=>{const r=e.getBoundingClientRect();return r.bottom>innerHeight+1||r.right>innerWidth+1||r.left<0}));
  assert.equal(clipped,false,`clipping at ${width}x${height}`);
  assert.equal(await page.evaluate(()=>document.querySelector('.stage').scrollHeight>document.querySelector('.stage').clientHeight+1),false,`stage overflow at ${width}x${height}`);
  if(width===550)await page.screenshot({path:output+'/muscle-compact.png'});
 }
 assert.deepEqual(errors,[]);console.log('Muscle: four variants, step controls, geometry, replay, cancellation, reset and responsive layout passed.');
} finally {await browser.close()}
