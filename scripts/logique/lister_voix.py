"""Pistes à mettre en voix d'un cours en attente → backend/data/curriculum/architecture/<deck>_voix.json,
et mots rares (même règle que scripts/voix/verifier_mots.py) sur chacune, observations comprises."""
import hashlib, json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(R / "scripts/voix"), str(R / "backend/kaggle_tts")]
from pistes_cours import pistes
from texte_parle import parle

deck = sys.argv[1]
m = json.load(open(R / f"backend/data/courses/en_attente/{deck}.json", encoding="utf-8"))
F = json.load(open(R / "backend/data/voix/frequences_corpus_v4.json", encoding="utf-8"))["mots"]
H = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()
D = {s["id"]: s for a in m["activities"] for s in a["slides"]}
out = []
for d, i, t, poser in pistes(m):
    if d == "mixed":
        a = (D[i].get("audio") or {}).get("mixed") or {}
        if a.get("url") and a.get("speech_hash") == H(t):
            continue
        out.append({"type": "diapositive", "id": i, "texte": t})
        continue
    obj = next((c.cell_contents for c in (poser.__closure__ or ()) if isinstance(c.cell_contents, dict)), {})
    if obj.get("enonce_audio" if i.startswith("enonce_") else "audio"):
        continue
    out.append({"type": {"reponses": "enonce" if i.startswith("enonce_") else "reaction", "demos": "demonstration"}[d],
                "id": i, "texte": t})
for s in D.values():
    o = (s.get("concentration") or {}).get("observation")
    if not o:
        continue
    b = f"enonce_obs_{s['id']}"
    if not o.get("enonce_audio"):
        out.append({"type": "observation", "id": f"{b}_q", "texte": o.get("enonce_dit") or o["enonce"]})
    for k, x in enumerate(o.get("indices") or []):
        if not x.get("audio"):
            out.append({"type": "observation", "id": f"{b}_i{k}", "texte": x.get("dit") or x["texte"]})
    for k, x in enumerate(o.get("retours") or []):
        if not x.get("audio"):
            out.append({"type": "observation", "id": f"{b}_r{k}", "texte": x["parole"]})
    so = o.get("solution") or {}
    if so.get("parole") and not so.get("audio"):
        out.append({"type": "observation", "id": f"{b}_s", "texte": so["parole"]})

MOT = re.compile(r"[ء-ي]+|[a-zà-ÿ'-]+")
PRE = ("وال", "فال", "بال", "لل", "ال", "و", "ف", "ب", "ل")


def freq(w):
    if re.match(r"[ء-ي]", w):
        return max([F.get(w, 0)] + [F.get(w[len(p):], 0) for p in PRE if w.startswith(p) and len(w) - len(p) >= 2])
    return F.get(re.sub(r"^(l|d|qu|n|s|j|c)'", "", w).strip("'-"), 0)


rares = {}
for p in out:
    for w in set(MOT.findall(parle(p["texte"]).lower().replace("’", "'"))):
        if len(w) >= 3 and freq(w) < 3:
            rares.setdefault(w, []).append(p["id"])
json.dump({"deck": deck, "pistes": out}, open(R / f"backend/data/curriculum/architecture/{deck}_voix.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), "pistes", dict(Counter(p["type"] for p in out)))
for w, ids in sorted(rares.items()):
    print(f"  {w} ({freq(w)}) : {', '.join(ids[:4])}{' …' if len(ids) > 4 else ''}")
