import json, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
D = json.load(open(r'backend/data/courses/math_ch1_limites_continuite.json', encoding='utf-8'))
BASE = 'http://127.0.0.1:8898'
SETUP = "() => { window.__e = []; addEventListener('message', e => { if (e.data && e.data.type === 'simulation_state') window.__e.push(e.data.current_state); }); }"
def cmd(pg, c, p=None):
    pg.evaluate("([c,p]) => postMessage({type:'simulation_control', command:c, parameters:p||{}}, '*')", [c, p]); pg.wait_for_timeout(150)
def etat(pg): return pg.evaluate("() => window.__e[window.__e.length-1]")
def attendre(pg):
    for _ in range(300):
        s = etat(pg)
        if s and s['simulation_status'] != 'running': return s
        pg.wait_for_timeout(150)
    return etat(pg)
probs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', args=['--headless=new'])
    SEULES = set(sys.argv[1:])
    for a in D['activities']:
        for s in a['slides']:
            v = s['visual']
            if SEULES and s['id'] not in SEULES: continue
            if v.get('kind') != 'simulation': continue
            c = s['concentration']
            pg = b.new_page(viewport={'width': 1000, 'height': 620}); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(BASE + v['url']); pg.evaluate(SETUP); pg.wait_for_timeout(500)
            st = None
            for _ in range(20):
                cmd(pg, 'pause' if _ % 2 == 0 else 'start'); pg.wait_for_timeout(250); st = etat(pg)
                if st: break
            if not st: probs.append(f"{s['id']}: pas d'état"); pg.close(); continue
            reps = set()
            etapes = [x for x in c['pointage']] + [x for x in (c.get('variante') or {}).get('etapes', [])]
            for x in etapes:
                if x.get('commande') == 'play_until':
                    m = x['parametres']['moment']; M = (etat(pg) or {}).get('moments', {})
                    if m not in M: probs.append(f"{s['id']}: moment inconnu {m} (connus : {list(M)})"); continue
                    cmd(pg, 'play_until', {'moment': m}); attendre(pg)
                elif x.get('commande'):
                    cmd(pg, x['commande'], x.get('parametres') or {}); pg.wait_for_timeout(300)
                reps |= set(pg.evaluate("() => Object.keys((window.Tableau.listeReperes && window.Tableau.listeReperes()) || {})"))
                if x.get('repere') and x['repere'] not in reps:
                    # le repère peut apparaître plus tard : on joue jusqu'à la fin et on revérifie
                    pass
            M = (etat(pg) or {}).get('moments', {})
            if 'fin' in M: cmd(pg, 'play_until', {'moment': 'fin'}); attendre(pg)
            reps |= set(pg.evaluate("() => Object.keys((window.Tableau.listeReperes && window.Tableau.listeReperes()) || {})"))
            for x in etapes:
                if x.get('repere') and x['repere'] not in reps: probs.append(f"{s['id']}: repère absent {x['repere']} (vus : {sorted(reps)})")
            enc = pg.evaluate("() => { const c=document.querySelector('canvas'); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0; for(let i=3;i<d.length;i+=16) if(d[i]>0) n++; return n; }")
            hors = pg.evaluate("() => (window.__horsCadre||[]).length")
            if errs: probs.append(f"{s['id']}: erreurs {errs[:2]}")
            if enc < 500: probs.append(f"{s['id']}: peu d'encre {enc}")
            if hors: probs.append(f"{s['id']}: {hors} textes hors cadre")
            print(s['id'], 'ok' if not errs else 'ERR', enc, (etat(pg) or {}).get('ce_qui_se_voit', '')[:110])
            pg.close()
    b.close()
print('\n'.join(probs) or 'AUCUN PROBLÈME')
