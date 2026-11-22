"""Aperçu des figures d'un exercice (énoncé + semblable) en PNG, pour vérifier les schémas et les courbes à l'œil.
Rendu proche de FigureCahier.tsx (craie sur fond sombre) — un contrôle, pas le rendu final.
Usage : python -X utf8 scripts/exercices/apercu.py frontend/public/media/exercices/<id>.json <dossier_png>"""
import json, math, sys, re
from pathlib import Path

C = {'blanc': '#eef2f6', 'cyan': '#22d3ee', 'jaune': '#facc15', 'vert': '#4ade80', 'violet': '#c084fc', 'orange': '#fb923c',
     'bleu': '#60a5fa', 'rouge': '#f87171', 'rose': '#f472b6', 'faible': 'rgba(226,232,240,.55)'}
W = 400


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def ev(expr, x):
    js = expr.replace('−', '-').replace('·', '*').replace('×', '*').replace('^', '**')
    env = {'exp': math.exp, 'ln': math.log, 'log': math.log10, 'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
           'tan': math.tan, 'abs': abs, 'atan': math.atan, 'pi': math.pi, 'x': x, 'floor': math.floor}
    return eval(js, {"__builtins__": {}}, env)


def svg_figure(f):
    if f.get('axes'):
        ax, ay = f['axes']['x'], f['axes']['y']
        x0, x1, y0, y1 = ax['min'], ax['max'], ay['min'], ay['max']
        ratio = f.get('ratio', 0.6)
        mg = 40
    else:
        x0, x1, y0, y1 = 0, f['cadre']['l'], 0, f['cadre']['h']
        ratio = f.get('ratio', f['cadre']['h'] / f['cadre']['l'])
        mg = 10
    H = W * ratio
    sx = lambda x: mg + (x - x0) / (x1 - x0) * (W - 2 * mg)
    sy = lambda y: H - mg - (y - y0) / (y1 - y0) * (H - 2 * mg)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*2}" height="{(H+40)*2}" viewBox="0 -30 {W} {H+40}" style="background:#1f2a24;font-family:Patrick Hand,cursive">']
    out.append(f'<text x="{W/2}" y="-12" fill="#facc15" font-size="15" text-anchor="middle">{esc(f.get("titre",""))}</text>')
    if f.get('axes'):
        out.append(f'<line x1="{sx(x0)}" y1="{sy(max(y0,0) if y0<0<y1 else y0)}" x2="{sx(x1)}" y2="{sy(max(y0,0) if y0<0<y1 else y0)}" stroke="#eee"/>')
        out.append(f'<line x1="{sx(x0)}" y1="{sy(y0)}" x2="{sx(x0)}" y2="{sy(y1)}" stroke="#eee"/>')
        out.append(f'<text x="{sx(x1)}" y="{sy(0 if y0<0<y1 else y0)+15}" fill="#eee" font-size="12">{esc(ax["nom"])} ({esc(ax.get("unite",""))})</text>')
        out.append(f'<text x="{sx(x0)+4}" y="{sy(y1)-4}" fill="#eee" font-size="12">{esc(ay["nom"])} ({esc(ay.get("unite",""))})</text>')
        for g in ax.get('graduations', []):
            v, t = (g if isinstance(g, list) else (g, str(g)))
            out.append(f'<text x="{sx(v)}" y="{sy(0 if y0<0<y1 else y0)+14}" fill="#aaa" font-size="10" text-anchor="middle">{esc(str(t))}</text>')
        for g in ay.get('graduations', []):
            v, t = (g if isinstance(g, list) else (g, str(g)))
            out.append(f'<text x="{sx(x0)-3}" y="{sy(v)+3}" fill="#aaa" font-size="10" text-anchor="end">{esc(str(t))}</text>')
    for e in f.get('elements', []):
        col = C.get(e.get('couleur', 'blanc'), '#eee')
        dash = ' stroke-dasharray="4 3"' if e.get('trait') == 'pointille' else ''
        k = e['f']
        if k == 'courbe':
            a, b = e.get('de', x0), e.get('a', x1)
            p = []
            for i in range(201):
                x = a + (b - a) * i / 200
                try: y = ev(e['expr'], x)
                except Exception: continue
                p.append(f'{sx(x):.1f},{sy(y):.1f}')
            out.append(f'<polyline points="{" ".join(p)}" fill="none" stroke="{col}" stroke-width="2"{dash}/>')
            if e.get('texte'):
                tx = e.get('texte_x', b)
                out.append(f'<text x="{sx(tx)}" y="{sy(ev(e["expr"], tx))-6}" fill="{col}" font-size="12">{esc(e["texte"])}</text>')
        elif k == 'ligne':
            p = ' '.join(f'{sx(q[0]):.1f},{sy(q[1]):.1f}' for q in e['pts'])
            tag = 'polygon' if e.get('ferme') else 'polyline'
            fill = C.get(e['remplir']) if e.get('remplir') else 'none'
            out.append(f'<{tag} points="{p}" fill="{fill}" stroke="{col}" stroke-width="{3 if e.get("epais") else 1.6}"{dash}/>')
        elif k in ('fleche', 'cote'):
            a, b = e['de'], e['a']
            out.append(f'<line x1="{sx(a[0])}" y1="{sy(a[1])}" x2="{sx(b[0])}" y2="{sy(b[1])}" stroke="{col}" stroke-width="1.6"{dash}/>')
            out.append(f'<circle cx="{sx(b[0])}" cy="{sy(b[1])}" r="3" fill="{col}"/>')
            if k == 'cote': out.append(f'<circle cx="{sx(a[0])}" cy="{sy(a[1])}" r="3" fill="{col}"/>')
            t = e.get('texte') or e.get('t')
            if t: out.append(f'<text x="{(sx(a[0])+sx(b[0]))/2}" y="{(sy(a[1])+sy(b[1]))/2-6}" fill="{col}" font-size="12" text-anchor="middle">{esc(t)}</text>')
        elif k in ('cercle',):
            r = e['r'] / (x1 - x0) * (W - 2 * mg)
            fill = C.get(e['remplir']) if e.get('remplir') else 'none'
            out.append(f'<circle cx="{sx(e["c"][0])}" cy="{sy(e["c"][1])}" r="{r}" fill="{fill}" stroke="{col}" stroke-width="1.6"/>')
        elif k == 'ellipse':
            rx = e['rx'] / (x1 - x0) * (W - 2 * mg); ry = e['ry'] / (y1 - y0) * (H - 2 * mg)
            out.append(f'<ellipse cx="{sx(e["c"][0])}" cy="{sy(e["c"][1])}" rx="{rx}" ry="{ry}" fill="none" stroke="{col}"/>')
        elif k == 'rect':
            a, b = e['de'], e['a']
            fill = C.get(e['remplir']) if e.get('remplir') else 'none'
            out.append(f'<rect x="{sx(a[0])}" y="{sy(b[1])}" width="{sx(b[0])-sx(a[0])}" height="{sy(a[1])-sy(b[1])}" fill="{fill}" stroke="{col}" stroke-width="1.6"{dash}/>')
        elif k == 'arc':
            r = e['r'] / (x1 - x0) * (W - 2 * mg)
            a0, a1 = math.radians(e['de']), math.radians(e['a'])
            cx, cy = sx(e['c'][0]), sy(e['c'][1])
            p1 = (cx + r * math.cos(a0), cy - r * math.sin(a0)); p2 = (cx + r * math.cos(a1), cy - r * math.sin(a1))
            large = 1 if (e['a'] - e['de']) % 360 > 180 else 0
            out.append(f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{r:.1f},{r:.1f} 0 {large} 0 {p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="{col}" stroke-width="1.6"/>')
        elif k == 'texte':
            anc = {'gauche': 'start', 'centre': 'middle', 'droite': 'end'}.get(e.get('ancre', 'gauche'), 'start')
            out.append(f'<text x="{sx(e["at"][0])}" y="{sy(e["at"][1])}" fill="{col}" font-size="13" text-anchor="{anc}">{esc(e["t"])}</text>')
        elif k == 'point':
            fill = 'none' if e.get('creux') else col
            out.append(f'<circle cx="{sx(e["at"][0])}" cy="{sy(e["at"][1])}" r="3" fill="{fill}" stroke="{col}"/>')
            if e.get('t'):
                d = {'n': (0, -8), 's': (0, 15), 'e': (7, 4), 'o': (-7, 4), 'ne': (6, -6), 'no': (-6, -6), 'se': (6, 14), 'so': (-6, 14)}.get(e.get('pos', 'ne'), (6, -6))
                out.append(f'<text x="{sx(e["at"][0])+d[0]}" y="{sy(e["at"][1])+d[1]}" fill="{col}" font-size="13" text-anchor="middle">{esc(e["t"])}</text>')
        elif k == 'repere':
            if e.get('x') is not None and e.get('y') is not None:
                out.append(f'<polyline points="{sx(e["x"])},{sy(y0)} {sx(e["x"])},{sy(e["y"])} {sx(x0)},{sy(e["y"])}" fill="none" stroke="{col}" stroke-dasharray="3 3"/>')
            elif e.get('x') is not None:
                out.append(f'<line x1="{sx(e["x"])}" y1="{sy(y0)}" x2="{sx(e["x"])}" y2="{sy(y1)}" stroke="{col}" stroke-dasharray="3 3"/>')
            elif e.get('y') is not None:
                out.append(f'<line x1="{sx(x0)}" y1="{sy(e["y"])}" x2="{sx(x1)}" y2="{sy(e["y"])}" stroke="{col}" stroke-dasharray="3 3"/>')
            if e.get('t'):
                out.append(f'<text x="{sx(e.get("x") or x1)}" y="{sy(e.get("y") or y0)-4}" fill="{col}" font-size="11">{esc(e["t"])}</text>')
    if f.get('legende'):
        out.append(f'<text x="4" y="{H+8}" fill="#aaa" font-size="10">{esc(f["legende"][:90])}</text>')
    out.append('</svg>')
    return '\n'.join(out)


if __name__ == '__main__':
    e = json.load(open(sys.argv[1], encoding='utf-8'))
    d = Path(sys.argv[2]); d.mkdir(parents=True, exist_ok=True)
    figs = e['enonce'].get('figures', []) + e['similaire']['enonce'].get('figures', [])
    html = '<html><body style="background:#111">' + ''.join(f'<div>{svg_figure(f)}</div>' for f in figs) + '</body></html>'
    p = d / (e['id'] + '.html'); p.write_text(html, encoding='utf-8')
    import subprocess
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:820,height:600}});"
          f"await pg.goto({json.dumps(p.resolve().as_uri())});await pg.screenshot({{path:{json.dumps(str(d / (e['id'] + '.png')))},fullPage:true}});await b.close();}})()")
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    print('png :', d / (e['id'] + '.png') if r.returncode == 0 else ('échec : ' + r.stderr[-300:]))
