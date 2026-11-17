"""Contrôle en navigateur (headless) du pointage d'un cours : la baguette tombe-t-elle sur l'objet nommé ?

Pour chaque diapositive à simulation, rejoue le pointage dans l'ordre de la parole :
  - `play_until` est envoyé à la simulation, on attend qu'elle s'arrête ;
  - pour chaque `repere`, on vérifie qu'il existe À CET INSTANT (sinon la baguette ne sait où aller ou montre un vide)
    et on découpe la zone montrée (avec la phrase dite) dans une planche HTML à relire d'un coup d'œil.
Prérequis : un serveur statique sur frontend/public (ex. python -m http.server 8772 --directory frontend/public).
Usage : python scripts/verifier_baguette.py backend/data/courses/<cours>.json [--base http://localhost:8772] [--sortie dossier] [--diapo id]
"""
import argparse, base64, html, json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def phrase_autour(parole, mot):
    i = parole.find(mot)
    if i < 0:
        return None
    fins = [k for k in (parole.find('.', i + len(mot)), parole.find('؟', i + len(mot)), parole.find('?', i + len(mot))) if k > 0]
    return parole[i:(min(fins) + 1 if fins else len(parole))].strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cours'); ap.add_argument('--base', default='http://localhost:8772')
    ap.add_argument('--sortie', default=None); ap.add_argument('--diapo', default=None)
    a = ap.parse_args()
    cours = json.loads(Path(a.cours).read_text(encoding='utf-8'))
    sortie = Path(a.sortie or f"verif_baguette_{Path(a.cours).stem}"); sortie.mkdir(parents=True, exist_ok=True)
    lignes, defauts = [], 0
    with sync_playwright() as pw:
        nav = None
        for canal in ('chrome', 'msedge', None):
            try:
                nav = pw.chromium.launch(channel=canal) if canal else pw.chromium.launch(); break
            except Exception:
                continue
        page = nav.new_page(viewport={'width': 1366, 'height': 613})
        for act in cours.get('activities', []):
            for s in act.get('slides', []):
                pts = (s.get('concentration') or {}).get('pointage') or []
                url = (s.get('visual') or {}).get('url', '')
                if not pts or '.html' not in url or (a.diapo and s.get('id') not in a.diapo.split(',')):
                    continue
                parole = (s.get('speech_text') or {}).get('mixed') or (s.get('speech_text') or {}).get('fr') or ''
                page.goto(a.base + url); page.wait_for_timeout(700)
                demarrer = (s.get('concentration') or {}).get('demarrer')
                if demarrer:
                    page.evaluate("c => window.executeAICommand && executeAICommand(c, {})", demarrer)
                lignes.append(f"<h2>{html.escape(s['id'])} — {html.escape(s.get('title',''))} <small>{html.escape(url.split('/')[-1])}</small></h2>")
                duree = (((s.get('audio') or {}).get('mixed') or {}).get('duration_ms') or 0) / 1000
                debut = page.evaluate("() => performance.now()") / 1000
                def attendre_mot(mot, avance=0.0):
                    # comme le lecteur (CourseFocusStage.instant) : instant ∝ position du mot dans la parole
                    if not duree:
                        return
                    i = parole.find(mot)
                    cible = max(0.0, i / max(1, len(parole)) * duree - 0.3 - avance)
                    reste = cible - (page.evaluate("() => performance.now()") / 1000 - debut)
                    if reste > 0:
                        page.wait_for_timeout(int(reste * 1000))
                ordre = sorted(pts, key=lambda p: (parole.find(p.get('mot', '')) if parole.find(p.get('mot', '')) >= 0 else 10**9))
                for p in ordre:
                    mot = p.get('mot', '')
                    dit = phrase_autour(parole, mot)
                    if dit is None:
                        defauts += 1; lignes.append(f"<p class=err>mot introuvable dans la parole : {html.escape(mot)}</p>"); continue
                    attendre_mot(mot, 0.9 if p.get('commande') else 0.0)
                    if p.get('commande'):
                        page.evaluate("([c, q]) => executeAICommand(c, q || {})", [p['commande'], p.get('parametres')])
                        page.wait_for_timeout(900)
                    if p.get('repere'):
                        r = p['repere']
                        # comme le lecteur : le repère est attendu jusqu'à 3 s après le mot (professor-locate.js), puis on regarde 0,8 s plus tard
                        page.wait_for_timeout(300)
                        for _ in range(25):
                            if page.evaluate("id => !!(window.Tableau && Tableau.rectRepere && Tableau.rectRepere(id))", r):
                                break
                            page.wait_for_timeout(120)
                        page.wait_for_timeout(800)
                        rect = page.evaluate("id => { const R = window.Tableau && Tableau.REPERES && Tableau.REPERES[id]; if (R) { const b = R.rect.getBoundingClientRect ? R.rect.getBoundingClientRect() : R.rect; return {x:b.x,y:b.y,w:b.width,h:b.height,label:R.label}; } const el = document.querySelector('[data-professor-point~=\"'+id+'\"],[data-repere=\"'+id+'\"]') || document.getElementById('hot-'+id); if (!el) return null; const b = el.getBoundingClientRect(); return {x:b.x,y:b.y,w:b.width,h:b.height,label:id}; }", r)
                        if not rect or rect['w'] < 2:
                            defauts += 1
                            lignes.append(f"<p class=err>« {html.escape(dit)} » → repère <b>{html.escape(r)}</b> ABSENT à cet instant</p>"); continue
                        m = 30
                        clip = {'x': max(0, rect['x'] - m), 'y': max(0, rect['y'] - m), 'width': min(1366, rect['w'] + 2 * m), 'height': min(613, rect['h'] + 2 * m)}
                        page.evaluate("([x,y,w,h]) => { const d=document.createElement('div'); d.id='__cadre'; Object.assign(d.style,{position:'fixed',left:x+'px',top:y+'px',width:w+'px',height:h+'px',border:'3px solid #f0f',zIndex:99999,pointerEvents:'none'}); document.body.appendChild(d); }", [rect['x'], rect['y'], rect['w'], rect['h']])
                        img = page.screenshot(clip=clip)
                        page.evaluate("() => document.getElementById('__cadre')?.remove()")
                        n = sum(1 for _ in sortie.glob('*.png')) + 1
                        (sortie / f"{n:03d}_{s['id']}_{r}.png").write_bytes(img)
                        print(f"{n:03d} {s['id']} | {dit[:70]} -> {r}")
                        b64 = base64.b64encode(img).decode()
                        lignes.append(f"<div class=c><img src='data:image/png;base64,{b64}'><p dir=auto>« {html.escape(dit)} »<br>→ <b>{html.escape(r)}</b> : {html.escape(rect['label'] or '')}</p></div>")
        nav.close()
    (sortie / 'planche.html').write_text("<meta charset=utf-8><style>body{background:#111;color:#eee;font:14px sans-serif}.c{display:inline-block;vertical-align:top;width:420px;margin:6px;background:#222;padding:6px}.c img{max-width:100%}.err{color:#f66}</style>" + '\n'.join(lignes), encoding='utf-8')
    print(f"{defauts} défaut(s). Planche : {sortie / 'planche.html'}")
    return 1 if defauts else 0

if __name__ == '__main__':
    sys.exit(main())
