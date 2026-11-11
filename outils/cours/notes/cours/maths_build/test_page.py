"""Teste des pages de simulation en headless : python test_page.py [--shot dossier] <url relative>…
Serveur statique attendu : python -m http.server 8898 -d frontend/public (lancé à part)."""
import json, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
BASE = 'http://127.0.0.1:8898'
args = sys.argv[1:]; shot = None
if args and args[0] == '--shot': shot = args[1]; args = args[2:]
SETUP = "() => { window.__e = []; addEventListener('message', e => { if (e.data && e.data.type === 'simulation_state') window.__e.push(e.data.current_state); }); }"
def cmd(pg, c, p=None): pg.evaluate("([c,p]) => postMessage({type:'simulation_control', command:c, parameters:p||{}}, '*')", [c, p]); pg.wait_for_timeout(120)
def etat(pg): return pg.evaluate("() => window.__e[window.__e.length-1]")
def attendre(pg):
    for _ in range(400):
        s = etat(pg)
        if s and s['simulation_status'] != 'running': return s
        pg.wait_for_timeout(100)
    return etat(pg)
pb = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', args=['--headless=new'])
    for u in args:
        pg = b.new_page(viewport={'width': 1000, 'height': 600}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(BASE + u); pg.evaluate(SETUP); pg.wait_for_timeout(400)
        cmd(pg, 'pause'); s = etat(pg) or {}
        M = s.get('moments', {})
        for m in sorted(M, key=M.get):
            cmd(pg, 'play_until', {'moment': m}); s = attendre(pg)
        enc = pg.evaluate("() => { const c=document.querySelector('canvas'); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0; for(let i=3;i<d.length;i+=16) if(d[i]>0) n++; return n; }")
        hors = pg.evaluate("() => window.__horsCadre||[]")
        reps = pg.evaluate("() => Object.keys(window.Tableau.listeReperes())")
        print('==', u, '| encre', enc, '| moments', list(M), '\n   repères', reps, '\n   vu:', (s or {}).get('ce_qui_se_voit', '')[:400])
        if errs: pb.append(f'{u}: erreurs {errs[:3]}')
        if enc < 500: pb.append(f'{u}: peu d’encre')
        if hors: pb.append(f'{u}: hors cadre {hors}')
        if shot: pg.screenshot(path=f"{shot}/{u.split('/')[-1].replace('?','_').replace('=','-').replace('&','_')}.png")
        pg.close()
    b.close()
print('\n'.join(pb) or 'AUCUN PROBLÈME')
