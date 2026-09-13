import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {mkdirSync,readFileSync} from 'node:fs';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{channel:'msedge'})});
mkdirSync('tmp/muscle-structure',{recursive:true});
try {
 const page=await browser.newPage({viewport:{width:1100,height:760}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto((process.env.TEST_BASE_URL||'http://127.0.0.1:5173')+'/visual-lab.html?scene=muscle-structure');
 await page.locator('.structure-canvas canvas').waitFor();
 await page.waitForTimeout(1500);
 await page.locator('[data-model-loaded="true"]').waitFor();
 for(const name of ['muscle','fascicle','fiber','myofibril','sarcomere']) {
  const buffer=readFileSync(`frontend/public/media/models/svt/muscle/${name}.glb`);
  assert.equal(buffer.toString('ascii',0,4),'glTF');
  assert.ok(buffer.length<8*1024*1024,'Keep each magnification below 8 MiB');
  const json=JSON.parse(buffer.toString('utf8',20,20+buffer.readUInt32LE(12)));
  assert.ok(json.meshes.length<16,'Anatomical grouping must limit draw calls');
  assert.ok(json.nodes.some(n=>n.extras?.anatomical_label));
  assert.ok((json.images||[]).every(image=>!image.uri),'Textures must be embedded');
  if(name!=='sarcomere')assert.ok(json.materials.some(m=>m.normalTexture),'Tissue must include surface relief');
 }
 const picture=()=>page.locator('.structure-canvas canvas').screenshot();
 const before=await picture();
 const box=await page.locator('canvas').boundingBox();
 await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);await page.mouse.down();await page.mouse.move(box.x+box.width*.7,box.y+box.height*.6,{steps:10});await page.mouse.up();await page.waitForTimeout(700);
 assert.notDeepEqual(await picture(),before,'Orbit must change rendered geometry');
 await page.locator('.structure-canvas').dblclick();await page.waitForTimeout(150);
 await page.mouse.click(box.x+box.width*.5,box.y+box.height*.5);assert.match(await page.locator('.structure-selected').textContent(),/Élément touché/);
 await page.getByRole('button',{name:'Fermer la coupe'}).click();assert.equal(await page.getByRole('button',{name:'Ouvrir la coupe'}).getAttribute('aria-pressed'),'false');
 const closed=await picture();
 await page.getByRole('button',{name:'Ouvrir la coupe'}).click();await page.waitForTimeout(200);assert.notDeepEqual(await picture(),closed,'The envelope must really open');
 for(const [i,name,step] of [[1,'Muscle',0],[2,'Faisceau',1],[3,'Fibre',2],[4,'Myofibrille',3],[5,'Sarcomère',5]]) {
  if(i>1)await page.getByRole('button',{name:'Niveau suivant',exact:true}).click();
  await page.locator('[data-model-loaded="true"]').waitFor();
  await page.waitForTimeout(350);
  assert.equal(await page.locator('.muscle-structure').getAttribute('data-stage-index'),String(step));
  assert.equal(await page.locator('canvas').count(),1);
  assert.ok(await page.locator('.muscle-structure button').count()<=3,'At most three controls');
  assert.equal(await page.evaluate(()=>getComputedStyle(document.querySelector('.muscle-structure')).backgroundColor),'rgba(0, 0, 0, 0)');
  assert.equal(await page.evaluate(()=>{const gl=document.querySelector('canvas').getContext('webgl2');return gl.getParameter(gl.COLOR_CLEAR_VALUE)[3]}),0,'The WebGL background must have zero alpha');
  await page.screenshot({path:`tmp/muscle-structure/${name}.png`});
 }
 for(const [width,height] of [[550,530],[390,700]]){
  await page.setViewportSize({width,height});await page.waitForTimeout(200);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth||document.documentElement.scrollHeight>innerHeight),false);
  assert.equal(await page.evaluate(()=>[...document.querySelectorAll('.muscle-structure button')].some(e=>e.getBoundingClientRect().bottom>innerHeight)),false);
  await page.screenshot({path:`tmp/muscle-structure/compact-${width}.png`});
 }
 await page.getByRole('button',{name:'Continuer vers le couplage'}).click();assert.equal(await page.locator('[data-stage-index]').getAttribute('data-stage-index'),'6');
 // A lost WebGL context gives a usable image and the level navigation remains operable.
 await page.goto((process.env.TEST_BASE_URL||'http://127.0.0.1:5173')+'/visual-lab.html?scene=muscle-structure');
 await page.locator('[data-model-loaded="true"]').waitFor();await page.locator('canvas').dispatchEvent('webglcontextlost');await page.locator('.structure-fallback').waitFor();
 assert.equal(await page.getByRole('button',{name:'Niveau suivant',exact:true}).isEnabled(),true);
 await page.route('**/media/models/svt/muscle/fiber.glb',route=>route.abort());
 await page.getByRole('button',{name:'Niveau suivant',exact:true}).click();await page.locator('[data-model-loaded="true"]').waitFor();await page.getByRole('button',{name:'Niveau suivant',exact:true}).click();await page.locator('.structure-fallback').waitFor();
 assert.equal(await page.locator('.structure-loading').count(),0,'A failed load must not leave an endless spinner');
 assert.deepEqual(errors,[]);console.log('3D muscle: five levels, real orbit, envelopes, navigation, responsive layout and WebGL fallback passed.');
}finally{await browser.close()}
