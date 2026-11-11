import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
S = r'C:/Users/HP/AppData/Local/Temp/claude/9269525a2680ed40/a857ffbb-cf28-4072-880f-f5ac5134ee69/scratchpad/shots'
B = 'http://127.0.0.1:8898/media/simulations/maths/limites-continuite-tableau/'
def cmd(pg, c, p=None): pg.evaluate("([c,p]) => postMessage({type:'simulation_control', command:c, parameters:p||{}}, '*')", [c, p]); pg.wait_for_timeout(1500)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', args=['--headless=new'])
    for page, ms in [('bilan.html', ['limites','continuite_point','continuite_intervalle','image','tvi','dichotomie','reciproque','courbe','racine']), ('carte.html', ['definition','limites','continuite','image','tvi','dichotomie','reciproque','courbe','racine'])]:
        pg = b.new_page(viewport={'width': 1000, 'height': 600}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and 'favicon' not in m.text and errs.append(m.text))
        pg.goto(B + page); pg.wait_for_timeout(800)
        for m in ms: cmd(pg, 'play_until', {'moment': m})
        pg.wait_for_timeout(6000)
        pg.screenshot(path=f'{S}/{page}_1.png')
        cmd(pg, 'set_parameters', {'lacunes': [{'id': 'K5', 'label': 'appliquer le théorème des valeurs intermédiaires', 'statut': 'non_acquis', 'reprendre_avec': ['simulation']}], 'acquis': ['calculer une limite'], 'acquis_ids': ['K1']})
        pg.wait_for_timeout(1500); pg.screenshot(path=f'{S}/{page}_2.png')
        if page == 'bilan.html': cmd(pg, 'play_until', {'moment': 'lacunes'}); pg.wait_for_timeout(2500); pg.screenshot(path=f'{S}/{page}_3.png')
        print(page, 'erreurs', errs[:3], 'hors', pg.evaluate("() => window.__horsCadre||[]"), 'deborde', pg.evaluate("() => window.__debordeBlocs||[]"))
        pg.close()
    b.close()
