// Teste des pages de simulation en headless (version node de maths_build/test_page.py, pour Linux) :
//   node outils/cours/notes/cours/maths_build/operations_formes/test_page.js [--shot dossier] <url relative>…
// Serveur statique attendu : python3 -m http.server 8898 -d frontend/public --bind 127.0.0.1 (lancé à part).
const { chromium } = require('playwright');
const BASE = 'http://127.0.0.1:8898';
let args = process.argv.slice(2); let shot = null;
if (args[0] === '--shot') { shot = args[1]; args = args.slice(2); }
const SETUP = "window.__e = []; addEventListener('message', e => { if (e.data && e.data.type === 'simulation_state') window.__e.push(e.data.current_state); });";
(async () => {
  const b = await chromium.launch(); const pb = [];
  const cmd = async (pg, c, p) => { await pg.evaluate(([c, p]) => postMessage({ type: 'simulation_control', command: c, parameters: p || {} }, '*'), [c, p]); await pg.waitForTimeout(120); };
  const etat = pg => pg.evaluate(() => window.__e[window.__e.length - 1]);
  const attendre = async pg => { for (let i = 0; i < 400; i++) { const s = await etat(pg); if (s && s.simulation_status !== 'running') return s; await pg.waitForTimeout(100); } return etat(pg); };
  for (const u of args) {
    const pg = await b.newPage({ viewport: { width: 1000, height: 600 } }); const errs = [];
    pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto(BASE + u); await pg.evaluate(SETUP); await pg.waitForTimeout(400);
    await cmd(pg, 'pause'); let s = (await etat(pg)) || {};
    const M = s.moments || {};
    for (const m of Object.keys(M).sort((x, y) => M[x] - M[y])) { await cmd(pg, 'play_until', { moment: m }); s = await attendre(pg); }
    const enc = await pg.evaluate(() => { const c = document.querySelector('canvas'); const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 16) if (d[i] > 0) n++; return n; });
    const hors = await pg.evaluate(() => window.__horsCadre || []);
    const reps = await pg.evaluate(() => Object.keys((window.Tableau.listeReperes && window.Tableau.listeReperes()) || {}));
    console.log('==', u, '| encre', enc, '| moments', Object.keys(M), '\n   repères', reps, '\n   vu:', String((s || {}).ce_qui_se_voit || '').slice(0, 400));
    if (errs.length) pb.push(`${u}: erreurs ${errs.slice(0, 3)}`);
    if (enc < 500) pb.push(`${u}: peu d’encre`);
    if (hors.length) pb.push(`${u}: hors cadre ${JSON.stringify(hors)}`);
    if (shot) await pg.screenshot({ path: `${shot}/${u.split('/').pop().replace(/[?=&]/g, '_')}.png` });
    await pg.close();
  }
  await b.close();
  console.log(pb.join('\n') || 'AUCUN PROBLÈME');
})();
