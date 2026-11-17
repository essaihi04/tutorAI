/*
 * Contrôle voix ↔ simulation dans un vrai navigateur (17 novembre 2026).
 *
 * Pour chaque diapositive à simulation d'un cours, ouvre la page de la simulation dans une iframe (comme le lecteur),
 * puis rejoue la voix en temps réel : chaque entrée de `concentration.pointage` part à l'instant où le lecteur
 * l'enverrait (place du mot dans la voix rapportée à la durée de la piste, 0,9 s plus tôt pour une commande, un geste
 * par seconde au plus). Il relève :
 *   - pour chaque `highlight` : le repère existe-t-il dans la scène à cet instant, son libellé, sa boîte, et une capture
 *     de la baguette (anneau de craie) posée dessus ;
 *   - pour chaque `play_until` : l'instant de la voix où la scène est arrivée et figée sur le moment, et ce qu'elle
 *     montre alors (`ce_qui_se_voit`) ;
 *   - les erreurs de la page.
 *
 * Usage (depuis frontend/) :
 *   node scripts/verifier-pointage-navigateur.mjs [cours.json] [--diapo id,id] [--sim chaine.html] [--sortie dossier]
 * Sortie : rapport texte sur la console + rapport.md et captures dans le dossier de sortie (par défaut
 * ../output/pointage/<cours>). Code de sortie 1 s'il y a un écart (repère absent, moment jamais atteint, erreur JS).
 */
import { createRequire } from 'node:module';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const { chromium } = createRequire(import.meta.url)('playwright');   // le Playwright installé (global ou du projet)
const ICI = path.dirname(fileURLToPath(import.meta.url));
const PUBLIC = path.resolve(ICI, '..', 'public');
const RACINE = path.resolve(ICI, '..', '..');
const args = process.argv.slice(2);
const opt = (nom) => { const i = args.indexOf(nom); if (i < 0) return null; const v = args[i + 1]; args.splice(i, 2); return v; };
const diapos = (opt('--diapo') || '').split(',').filter(Boolean);
const filtreSim = opt('--sim');
const sortieOpt = opt('--sortie');
const coursChemin = path.resolve(args[0] || path.join(RACINE, 'backend/data/courses/svt_ch1_reactions_responsables_liberation_energie.json'));
const cours = JSON.parse(fs.readFileSync(coursChemin, 'utf8'));
const sortie = path.resolve(sortieOpt || path.join(RACINE, 'output', 'pointage', cours.id));
fs.mkdirSync(sortie, { recursive: true });
const AVANCE = 0.9, GESTE = 1.0;

/* Un petit serveur statique de frontend/public (les pages chargent /media/simulations/shared/...). */
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.json': 'application/json', '.mp3': 'audio/mpeg' };
const serveur = http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  if (u.pathname === '/__banc') {
    res.writeHead(200, { 'content-type': TYPES['.html'] });
    res.end(`<!doctype html><html><body style="margin:0;background:#1f2a24"><iframe id="sim" src="${u.searchParams.get('src')}" style="border:0;width:1180px;height:540px;background:transparent"></iframe></body></html>`);
    return;
  }
  const f = path.join(PUBLIC, decodeURIComponent(u.pathname));
  if (!f.startsWith(PUBLIC) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
await new Promise(r => serveur.listen(0, r));
const BASE = `http://127.0.0.1:${serveur.address().port}`;

let ecarts = 0;

function plan(slide) {
  const parole = (slide.speech_text?.mixed || '').trim();
  const duree = (slide.audio?.mixed?.duration_ms || 0) / 1000;
  const instant = (mot) => { const i = parole.indexOf(mot); return i < 0 || !duree ? 0 : Math.max(0, (i / Math.max(1, parole.length)) * duree - 0.3); };
  const gestes = (slide.concentration?.pointage || []).map((p, i) => ({ ...p, i, t: Math.max(0, instant(p.mot) - (p.commande ? AVANCE : 0)), tMot: instant(p.mot) }));
  // un geste par seconde, dans l'ordre (comme parTuteur avec le tuteur 3D)
  let prochain = -1e9;
  for (const g of [...gestes].sort((a, b) => a.t - b.t || a.i - b.i)) { g.eff = Math.max(g.t, prochain); prochain = g.eff + GESTE; }
  return { parole, duree, gestes: gestes.sort((a, b) => a.eff - b.eff) };
}

async function verifierDiapo(navigateur, slide, lignes) {
  const dire = (s) => lignes.push(s);
  const { duree, gestes } = plan(slide);
  const url = slide.visual.url;
  const page = await navigateur.newPage({ viewport: { width: 1200, height: 560 } });
  const erreurs = [];
  page.on('pageerror', e => erreurs.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') erreurs.push(m.text()); });
  await page.goto(`${BASE}/__banc?src=${encodeURIComponent(url)}`);
  const cadre = await (await page.waitForSelector('#sim')).contentFrame();
  await cadre.waitForFunction(() => window.Tableau && window.executeAICommand, null, { timeout: 15000 });
  await page.waitForTimeout(900);
  const envoyer = (command, parameters = {}) => cadre.evaluate(([c, p]) => window.executeAICommand(c, p), [command, parameters]);
  const lireEtat = () => cadre.evaluate(() => (window.__etatTableau ? window.__etatTableau() : null));
  const dossier = path.join(sortie, slide.id); fs.mkdirSync(dossier, { recursive: true });
  dire(`\n== ${slide.id} — ${url} (voix ${duree.toFixed(1)} s)`);
  const t0 = Date.now();
  const voix = () => (Date.now() - t0) / 1000;
  if (slide.concentration?.demarrer) await envoyer(slide.concentration.demarrer);
  const attendus = [];   // play_until en cours : on note quand la scène se fige sur le moment
  const suivi = setInterval(async () => {
    try {
      const e = await lireEtat();
      if (!e) return;
      for (const a of attendus) if (a.atteint == null && e.simulation_status !== 'running' && Math.abs(e.time_s - a.cible) < 0.02) a.atteint = voix();
    } catch { /* page fermée */ }
  }, 100);
  for (const g of gestes) {
    const attente = g.eff - voix();
    if (attente > 0) await page.waitForTimeout(attente * 1000);
    if (g.commande) {
      const avant = await lireEtat();
      await envoyer(g.commande, g.parametres || {});
      await page.waitForTimeout(60);
      const apres = await lireEtat();
      const moments = apres?.moments || {};
      const m = g.parametres?.moment;
      let note = '';
      // la commande précédente, pas encore figée, est remplacée : la scène passe par son moment sans s'y arrêter
      for (const x of attendus) if (x.atteint == null && apres && x.cible <= (moments[m] ?? -1) + 1e-6 && x.cible <= (apres.time_s ?? 0) + 0.3) x.enchaine = voix();
      if (g.commande === 'play_until' && m) {
        if (!(m in moments)) { note = `  ✗ moment « ${m} » inconnu de la scène`; ecarts++; }
        else attendus.push({ g, cible: moments[m], m, depuis: avant?.time_s });
      }
      dire(`  ${voix().toFixed(1).padStart(5)}s  ${g.commande} ${JSON.stringify(g.parametres || {})}  [scène ${avant?.time_s ?? '?'} s → ${apres?.simulation_status}]  « ${g.mot} »${note}`);
    } else if (g.repere) {
      await envoyer('highlight', { target: g.repere });
      await page.waitForTimeout(250);
      const info = await cadre.evaluate((id) => {
        const r = window.Tableau.REPERES[id];
        const rect = window.Tableau.rectRepere(id);
        const anneau = document.querySelector('.repere-anneau');
        return { existe: !!r, label: r?.label, rect, anneau: !!anneau, t: window.__etatTableau ? window.__etatTableau().time_s : null };
      }, g.repere);
      const fichier = `${String(g.i).padStart(2, '0')}-${g.repere}.png`;
      await page.screenshot({ path: path.join(dossier, fichier) });
      const ok = info.existe && info.anneau;
      if (!ok) ecarts++;
      dire(`  ${voix().toFixed(1).padStart(5)}s  baguette → ${g.repere} ${ok ? '✓' : '✗ ABSENT'} « ${info.label || '—'} » [scène ${info.t?.toFixed?.(2)} s] (${fichier})  « ${g.mot} »`);
    }
  }
  const reste = duree - voix();
  if (reste > 0) await page.waitForTimeout(reste * 1000 + 300);
  clearInterval(suivi);
  for (const a of attendus) {
    if (a.atteint == null && a.enchaine != null) dire(`  · ${a.m} : traversé sans arrêt à ${a.enchaine.toFixed(1)} s de voix (la commande suivante a pris le relais)`);
    else if (a.atteint == null) { ecarts++; dire(`  ✗ ${a.m} (${a.cible} s de scène) jamais atteint pendant la voix`); }
    else dire(`  · ${a.m} : figé à ${a.atteint.toFixed(1)} s de voix (commande à ${a.g.eff.toFixed(1)} s, mot à ${a.g.tMot.toFixed(1)} s)`);
  }
  const fin = await lireEtat();
  dire(`  fin de la voix : ${fin?.ce_qui_se_voit?.slice(0, 220) || '—'}`);
  await page.screenshot({ path: path.join(dossier, 'fin.png') });
  for (const e of erreurs) { ecarts++; dire(`  ✗ erreur de la page : ${e}`); }
  await page.close();
}

const navigateur = await chromium.launch();
const choisies = [];
for (const a of cours.activities || []) for (const s of a.slides || []) {
  const u = s.visual?.url || '';
  if (s.visual?.kind !== 'simulation' || !u.includes('-tableau/')) continue;
  if (diapos.length && !diapos.includes(s.id)) continue;
  if (filtreSim && !u.includes(filtreSim)) continue;
  choisies.push(s);
}
// quatre diapositives à la fois (chacune dure le temps de sa voix)
const file = [...choisies];
const rapports = new Map();
await Promise.all(Array.from({ length: 4 }, async () => {
  while (file.length) {
    const s = file.shift();
    const l = [];
    try { await verifierDiapo(navigateur, s, l); } catch (e) { ecarts++; l.push(`✗ ${s.id} : ${e}`); }
    rapports.set(s.id, l);
    console.log(l.join('\n'));
  }
}));
await navigateur.close();
serveur.close();
const lignes = choisies.flatMap(s => rapports.get(s.id) || []);
fs.writeFileSync(path.join(sortie, 'rapport.md'), lignes.join('\n') + `\n\n${ecarts} écart(s)\n`);
console.log(`\n${ecarts} écart(s) — rapport et captures : ${sortie}`);
process.exit(ecarts ? 1 : 0);
