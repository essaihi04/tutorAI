import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

// Use the workspace's Playwright, or a bundled runtime supplied by the caller.
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
const url = (process.env.TEST_BASE_URL || 'http://localhost:5173') + '/media/simulations/svt/ch1_consommation_matiere_organique/exercices/ordre-respiration/index.html';
try {
  const page = await browser.newPage({ viewport: { width: 550, height: 530 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.addInitScript(() => {
    window.recorded = [];
    window.addEventListener('message', event => {
      if (event.data?.type === 'simulation_state') window.recorded.push(event.data);
    });
  });
  await page.goto(url);
  const state = () => page.evaluate(() => window.recorded.at(-1));
  const step = async (count = 4) => { for (let i = 0; i < count; i++) await page.locator('#next').click(); };
  const finish = async () => {
    await page.locator('#recycle').click(); await page.locator('#start').click();
    await page.waitForFunction(() => window.recorded.at(-1)?.current_state.simulation_status === 'finished');
  };
  await step();
  await page.locator('#start').click();
  assert.match(await page.locator('#feedback').textContent(), /attente/);
  assert.equal((await state()).current_state.glycolytic_nad_available, 0);
  assert.equal((await state()).current_state.second_glucose_started, false);
  await finish();
  assert.equal((await state()).current_state.simulation_status, 'finished');
  assert.equal((await state()).objective_progress, 0.5);
  await page.locator('#oxygen').click();
  await step(); await finish();
  assert.equal((await state()).objective_progress, 1);
  assert.equal((await state()).current_state.pathway, 'fermentation');
  await page.locator('#ethanol').click();
  assert.match(await page.locator('#productText').textContent(), /2 éthanols \+ 2 CO₂/);
  await page.locator('#oxygen').click();
  await page.locator('#mitochondria').click();
  await step(3);
  assert.match(await page.locator('#feedback').textContent(), /O₂ seul/);
  await page.locator('#enzyme').click();
  assert.equal(await page.locator('#enzymeInfo').isVisible(), true);
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('#enzymeInfo').isVisible(), false);
  await page.locator('#reset').click();
  assert.equal((await state()).objective_progress, 0);
  assert.equal((await state()).current_state.simulation_status, 'idle');

  // Native tutor commands, animation completion and cancellation.
  const command = async (command, parameters = {}) => {
    const count = await page.evaluate(() => window.recorded.length);
    await page.evaluate(({ command, parameters }) => window.postMessage({ type: 'simulation_control', simulation_id: 'ordre_respiration_svt', command, parameters }, '*'), { command, parameters });
    await page.waitForFunction(count => window.recorded.length > count, count);
  };
  await command('set_variant', { variant_id: 'respiration' });
  await page.waitForFunction(() => window.recorded.at(-1)?.current_state.stage === 4, null, { timeout: 12000 });
  await command('recycle'); await command('start');
  await page.waitForFunction(() => window.recorded.at(-1)?.current_state.simulation_status === 'finished');
  await command('reset'); await command('start'); await command('pause');
  const paused = (await state()).current_state.stage;
  await page.waitForTimeout(2600);
  assert.equal((await state()).current_state.stage, paused);
  await command('reset');
  await page.waitForTimeout(1800);
  assert.equal(await page.locator('#traveller').getAttribute('visibility'), 'hidden');

  // The document and controls fit both phone and embedded panel dimensions.
  for (const [width, height] of [[360, 640], [550, 430], [550, 748]]) {
    await page.setViewportSize({ width, height });
    const fits = await page.evaluate(() => {
      const controls = document.querySelector('.actions').getBoundingClientRect();
      return document.documentElement.scrollWidth <= innerWidth && document.documentElement.scrollHeight <= innerHeight && controls.bottom <= innerHeight && controls.right <= innerWidth;
    });
    assert.equal(fits, true, `Controls must fit ${width} × ${height}`);
  }
  assert.deepEqual(errors, []);
  console.log('PASS: both pathways, NAD regeneration gate, next glucose, ethanol, inactive mitochondrion, tutor commands, pause/reset and responsive controls.');
} finally {
  await browser.close();
}
