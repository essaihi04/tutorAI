// Même contrôle que verif_sims.py, en node (Playwright pour node, sans python) :
//   node outils/cours/notes/cours/etat_equilibre_build/verif_sims.js [slide_id …]   (serveur : python -m http.server 8931 -d frontend/public)
const fs = require('fs');
const { chromium } = require('playwright');
const D = JSON.parse(fs.readFileSync('backend/data/courses/phys_ch12_etat_equilibre.json', 'utf8'));
const BASE = 'http://127.0.0.1:8931';
const SETUP = "window.__e = []; addEventListener('message', e => { if (e.data && e.data.type === 'simulation_state') window.__e.push(e.data.current_state); });";
const SEULES = new Set(process.argv.slice(2));
(async () => {
  const b = await chromium.launch(); const probs = [];
  const cmd = async (pg, c, p) => { await pg.evaluate(([c, p]) => postMessage({ type: 'simulation_control', command: c, parameters: p || {} }, '*'), [c, p]); await pg.waitForTimeout(150); };
  const etat = pg => pg.evaluate(() => window.__e[window.__e.length - 1]);
  const attendre = async pg => { for (let i = 0; i < 300; i++) { const s = await etat(pg); if (s && s.simulation_status !== 'running') return s; await pg.waitForTimeout(150); } return etat(pg); };
  const reperes = pg => pg.evaluate(() => Object.keys((window.Tableau.listeReperes && window.Tableau.listeReperes()) || {}));
  for (const a of D.activities) for (const s of a.slides) {
    const v = s.visual; if (SEULES.size && !SEULES.has(s.id)) continue; if (v.kind !== 'simulation') continue;
    const c = s.concentration; const pg = await b.newPage({ viewport: { width: 1000, height: 620 } }); const errs = [];
    pg.on('pageerror', e => errs.push(String(e)));
    await pg.goto(BASE + v.url); await pg.evaluate(SETUP); await pg.waitForTimeout(500);
    let st = null;
    for (let i = 0; i < 20 && !st; i++) { await cmd(pg, i % 2 === 0 ? 'pause' : 'start'); await pg.waitForTimeout(250); st = await etat(pg); }
    if (!st) { probs.push(`${s.id}: pas d'état`); await pg.close(); continue; }
    const reps = new Set(); const etapes = [...c.pointage, ...((c.variante || {}).etapes || [])];
    for (const x of etapes) {
      if (x.commande === 'play_until') {
        const m = x.parametres.moment; const M = ((await etat(pg)) || {}).moments || {};
        if (!(m in M)) { probs.push(`${s.id}: moment inconnu ${m} (connus : ${Object.keys(M)})`); continue; }
        await cmd(pg, 'play_until', { moment: m }); await attendre(pg);
      } else if (x.commande) { await cmd(pg, x.commande, x.parametres || {}); await pg.waitForTimeout(300); }
      (await reperes(pg)).forEach(r => reps.add(r));
    }
    const M = ((await etat(pg)) || {}).moments || {};
    if ('fin' in M) { await cmd(pg, 'play_until', { moment: 'fin' }); await attendre(pg); }
    (await reperes(pg)).forEach(r => reps.add(r));
    for (const x of etapes) if (x.repere && !reps.has(x.repere)) probs.push(`${s.id}: repère absent ${x.repere} (vus : ${[...reps].sort()})`);
    const enc = await pg.evaluate(() => { const c = document.querySelector('canvas'); const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 16) if (d[i] > 0) n++; return n; });
    const hors = await pg.evaluate(() => (window.__horsCadre || []).length);
    if (errs.length) probs.push(`${s.id}: erreurs ${errs.slice(0, 2)}`);
    if (enc < 500) probs.push(`${s.id}: peu d'encre ${enc}`);
    if (hors) probs.push(`${s.id}: ${hors} textes hors cadre`);
    console.log(s.id, errs.length ? 'ERR' : 'ok', enc, (((await etat(pg)) || {}).ce_qui_se_voit || '').slice(0, 100));
    await pg.close();
  }
  await b.close();
  console.log(probs.join('\n') || 'AUCUN PROBLÈME');
})();
