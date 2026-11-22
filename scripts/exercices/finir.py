"""Passe finale d'un exercice : règle des nombres (texte_parle.nombres_darija_fr) sur TOUT texte dit (et ses « mot »),
puis contrôles : mots du pointage et de la correction présents dans la parole, aucun chiffre dans la voix."""
import json, re, sys, importlib.util
from pathlib import Path
# Usage (dans le dépôt) : python -X utf8 scripts/exercices/finir.py frontend/public/media/exercices/<id>.json [...]
TP = Path(__file__).resolve().parents[2] / "backend" / "kaggle_tts" / "texte_parle.py"
sp = importlib.util.spec_from_file_location("tp", TP); tp = importlib.util.module_from_spec(sp); sp.loader.exec_module(tp)
AR = re.compile(r"[\u0600-\u06FF]")
CHAMPS_VOIX = {"mixed", "dit", "parole", "intro_dit", "texte_dit", "enonce_dit", "mot"}
for f in sys.argv[1:]:
    e = json.load(open(f, encoding="utf-8")); pb = []
    def walk(o, k=""):
        if isinstance(o, dict): return {kk: walk(v, kk) for kk, v in o.items()}
        if isinstance(o, list): return [walk(v, k) for v in o]
        if isinstance(o, str) and k in CHAMPS_VOIX and AR.search(o):
            o = tp.nombres_darija_fr(o)
            if re.search(r"\d", o): pb.append(("chiffre", o[:70]))
        return o
    e = walk(e)
    for a in e["explication"]["activities"]:
        for s in a["slides"]:
            for p in s["concentration"].get("pointage", []) + s["concentration"].get("centre", []):
                if p["mot"] not in s["speech_text"]["mixed"]: pb.append(("mot absent", s["id"], p["mot"]))
    for q in e["enonce"]["questions"] + e["similaire"]["enonce"]["questions"]:
        for l in q["correction"]["lignes"]:
            if l["mot"] not in q["correction"]["parole"]: pb.append(("mot correction absent", q["id"], l["mot"]))
    json.dump(e, open(f, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print(f, "problèmes :", len(pb)); [print("  ", x) for x in pb]
