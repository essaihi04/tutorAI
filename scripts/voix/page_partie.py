import json, html, base64, subprocess, os, sys
part = sys.argv[1]
L = {x["cle"]: x["texte"] for x in json.load(open("liste.json", encoding="utf-8"))}
R = json.load(open("rapport.json", encoding="utf-8"))
items = sorted((0 if [x for n in r["notes"] for x in n["reste"]] else 1, c, r["notes"]) for c, r in R.items())
rows = []
for i, (k, cle, notes) in enumerate(items, 1):
    reste = [x for n in notes for x in n["reste"]]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"voix/{cle}.wav", "-ac", "1", "-b:a", "48k", "t.mp3"], check=True)
    src = "data:audio/mpeg;base64," + base64.b64encode(open("t.mp3", "rb").read()).decode(); os.remove("t.mp3")
    stt = " ".join(n.get("stt", "") for n in notes); ess = max(n["essais"] for n in notes)
    strat = ", ".join(sorted({n.get("strategie", "normal") for n in notes}))
    etat = f'<b class="ko">signalée</b><br><small>{html.escape("; ".join(reste))}</small>' if reste else '<b class="ok">juste</b>'
    rows.append(f'<tr><td>{i}</td><td><small>{html.escape(cle)}</small><br><audio controls preload="none" src="{src}"></audio></td><td dir="auto">{html.escape(L.get(cle, ""))}</td><td dir="auto" class="h">{html.escape(stt)}</td><td>{ess}<br><small>{strat}</small></td><td>{etat}</td></tr>')
n_ko = sum(1 for x in items if x[0] == 0)
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{html.escape(part)}</title><style>
:root{{--bg:#fff;--fg:#1d1d1f;--mut:#666;--li:#e5e5e5;--ko:#c62828;--ok:#1a7f37}}@media (prefers-color-scheme:dark){{:root{{--bg:#16171a;--fg:#eee;--mut:#9a9a9a;--li:#333;--ko:#ff6b6b;--ok:#5cc47a}}}}
body{{background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,sans-serif;margin:16px}}table{{border-collapse:collapse;width:100%}}
td{{border-top:1px solid var(--li);padding:8px;vertical-align:top;max-width:380px}}.h{{color:var(--mut)}}.ko{{color:var(--ko)}}.ok{{color:var(--ok)}}audio{{width:240px}}small{{color:var(--mut)}}</style></head><body>
<h1>{html.escape(part)} — {len(items)} pistes refaites avec la voix v6</h1>
<p>{n_ko} pistes encore signalées par le contrôle des nombres (en haut), {len(items) - n_ko} justes. Votre écoute décide : dites-moi les pistes à refaire et ce qui est mal dit. « prises » = nombre de prises (et façon gardée : normal, D, C).</p>
<table><tr><th>#</th><th>piste / audio</th><th>texte</th><th>MoulSot entend</th><th>prises</th><th>contrôle</th></tr>{"".join(rows)}</table></body></html>'''
open("ecoute.html", "w", encoding="utf-8").write(page); print("page", n_ko, "/", len(items))
