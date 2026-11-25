// Rejoue le pointage de chaque diapo du cours dans sa vraie simulation (Chromium) : moments, repères, observations,
// apres_reponse, allume des démonstrations, erreurs console. Prérequis : python3 -m http.server 8765 -d frontend/public
// Usage : node scripts/tcf/synthese/rejouer_diapos.js frontend/src/publication/tcf/cours/tc_chim_synthese.json [id_diapo]
// Rejoue le pointage de chaque diapo du cours dans sa simulation et contrôle moments, repères, erreurs.
const { chromium } = require('playwright');
const fs = require('fs');
const deck = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const seul = process.argv[3];
(async () => {
  const b = await chromium.launch(); let defauts = 0;
  for (const a of deck.activities) for (const s of a.slides) {
    if (s.visual.kind !== 'simulation' || (seul && s.id !== seul)) continue;
    const p = await b.newPage({ viewport: { width: 860, height: 420 } });
    const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' || /hors cadre|inconnu/.test(m.text())) errs.push(m.text()); });
    await p.goto('http://localhost:8765' + s.visual.url); await p.waitForTimeout(900);
    const etat = () => p.evaluate(() => window.__etatTableau());
    const reps = () => p.evaluate(() => Object.keys(window.Tableau.REPERES || {}));
    const envoyer = (command, parameters) => p.evaluate(([c, pa]) => window.postMessage({ type: 'simulation_control', command: c, parameters: pa }, '*'), [command, parameters]);
    const moments = (await etat()).moments || {};
    const pb = [];
    const c = s.concentration || {};
    const reserves = new Set([].concat(c.apres_reponse || []).flatMap(x => x.etapes || []).filter(e => e.commande === 'play_until').map(e => e.parametres.moment));
    const jouer = async (m) => {
      if (!(m in moments)) { pb.push('moment inconnu ' + m); return; }
      await envoyer('play_until', { moment: m });
      for (let i = 0; i < 40; i++) { await p.waitForTimeout(150); const e = await etat(); if (e.simulation_status !== 'running') break; }
      await p.waitForTimeout(900);
    };
    const repere = async (r) => { await p.waitForTimeout(300); const R = await reps(); if (!R.includes(r)) pb.push('repère absent ' + r + ' (présents : ' + R.join(',') + ')'); };
    const pts = c.pointage || [];
    const obs = c.observation; const posObs = obs ? s.speech_text.mixed.indexOf(obs.apres_mot) : -1;
    let obsFaite = false;
    if (c.apres_reponse) for (const x of [].concat(c.apres_reponse)) if (x.sim_avant) await envoyer('set_parameters', x.sim_avant);
    for (const pt of pts) {
      const pos = s.speech_text.mixed.indexOf(pt.mot);
      if (obs && !obsFaite && pos > posObs) {
        obsFaite = true; await envoyer('set_parameters', obs.sim_avant || {});
        for (const g of obs.gestes || []) { if (g.commande === 'play_until') await jouer(g.parametres.moment); else if (g.repere) await repere(g.repere); }
        for (const x of obs.indices) if (x.repere) await repere(x.repere);
        await envoyer('set_parameters', obs.sim_apres || {});
      }
      if (pt.commande === 'play_until') { if (reserves.has(pt.parametres.moment)) pb.push('moment réservé joué ' + pt.parametres.moment); await jouer(pt.parametres.moment); }
      else if (pt.commande === 'set_parameters') await envoyer('set_parameters', pt.parametres);
      else if (pt.repere) await repere(pt.repere);
    }
    for (const x of [].concat(c.apres_reponse || [])) for (const e of x.etapes) {
      if (e.commande === 'play_until') await jouer(e.parametres.moment); else if (e.commande === 'set_parameters') await envoyer('set_parameters', e.parametres); else if (e.repere) await repere(e.repere);
    }
    const q = s.question || {};
    for (const l of ((q.demonstration || {}).lignes || [])) for (const t of [].concat(l.allume || [])) { const R = await reps(); if (!R.includes(t) && !(t in moments)) pb.push('allume inconnu ' + t); }
    const vu = (await etat()).ce_qui_se_voit;
    if (errs.length) pb.push('console : ' + [...new Set(errs)].slice(0, 3).join(' | '));
    console.log((pb.length ? '✗ ' : '✓ ') + s.id + (pb.length ? '\n    ' + pb.join('\n    ') : '') + (process.env.VU ? '\n    vu : ' + vu : ''));
    defauts += pb.length; await p.close();
  }
  console.log('défauts :', defauts); await b.close();
})();
