"""Chaque `mot` (pointage, centre, démonstration) est un extrait exact de son texte parlé ; chaque bloc a au plus une
diapositive « À toi » (question ou exercices). Usage : python scripts/logique/verifier_mots_pointes.py <cours.json>"""
import json, sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
S = {s["id"]: s for a in d["activities"] for s in a["slides"]}
n = 0
for s in S.values():
    t = s["speech_text"]["mixed"]
    c = s.get("concentration") or {}
    for p in (c.get("pointage") or []) + (c.get("centre") or []):
        if not p.get("mot") or p["mot"] not in t:
            n += 1; print(f"{s['id']} : mot absent de la voix « {p.get('mot')} »")
    for q in [s.get("question")] + list(s.get("exercises") or []):
        dm = (q or {}).get("demonstration") or {}
        for l in dm.get("lignes") or []:
            if l["mot"] not in dm.get("parole", ""):
                n += 1; print(f"{s['id']} : démonstration, mot absent « {l['mot']} »")
for se in d["seances"]:
    for b in se["blocs"]:
        q = [i for i in b["slide_ids"] if S[i].get("question") or S[i].get("exercises")]
        if len(q) > 1:
            print(f"bloc {b['id']} : {len(q)} diapositives « À toi » ({', '.join(q)})")
print(f"--- {n} mot(s) introuvable(s)")
