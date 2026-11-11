"""Test rapide (set_time à la fin) : python vite.py <dossier captures> <url…> — moments, repères, erreurs, hors cadre, capture."""
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
BASE = 'http://127.0.0.1:8898'
shot, urls = sys.argv[1], sys.argv[2:]
SETUP = "() => { window.__e = []; addEventListener('message', e => { if (e.data && e.data.type === 'simulation_state') window.__e.push(e.data.current_state); }); }"
pb = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', args=['--headless=new'])
    for u in urls:
        pg = b.new_page(viewport={'width': 1000, 'height': 600}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(BASE + u); pg.evaluate(SETUP); pg.wait_for_timeout(500)
        pg.evaluate("() => postMessage({type:'simulation_control', command:'set_time', parameters:{time_s:1e5}}, '*')"); pg.wait_for_timeout(700)
        s = pg.evaluate("() => window.__e[window.__e.length-1]") or {}
        hors = pg.evaluate("() => window.__horsCadre||[]")
        reps = pg.evaluate("() => Object.keys(window.Tableau.listeReperes())")
        print('==', u, '\n   moments', list(s.get('moments', {})), '\n   repères', reps)
        if errs: pb.append(f'{u}: erreurs {errs[:3]}')
        if hors: pb.append(f'{u}: hors cadre {hors}')
        pg.screenshot(path=f"{shot}/{u.split('/')[-1].replace('?','_').replace('=','-').replace('&','_')}.png")
        pg.close()
    b.close()
print('\n'.join(pb) or 'AUCUN PROBLÈME')
