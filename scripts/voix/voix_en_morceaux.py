"""Voix d'une diapositive en deux morceaux (le tunnel coupe au-delà de ~100 s de calcul), recollés avec 0,3 s de
silence comme le fait le lot. Usage (sur le VPS) : python voix_en_deux.py URL DOSSIER ID"""
import io, json, re, sys, wave

import httpx

url, dossier, ident = sys.argv[1:4]
conf = json.load(open("/tmp/essai_conf.json"))
h = {"Authorization": "Bearer " + conf["jeton"]}
m = json.load(open(f"{dossier}/cours.json", encoding="utf-8"))
texte = next(s for a in m["activities"] for s in a["slides"] if s["id"] == ident)["speech_text"]["mixed"].strip()
coupes = [mt.end() for mt in re.finditer(r"[.!?؟]\s+", texte)]
n = max(2, -(-len(texte) // 320))          # morceaux d'environ 300 caractères (< 100 s de calcul chacun)
bornes = sorted({min(coupes, key=lambda c: abs(c - len(texte) * k / n)) for k in range(1, n)})
morceaux = [texte[a:b].strip() for a, b in zip([0] + bornes, bornes + [len(texte)])]
print(len(texte), "caractères ->", [len(x) for x in morceaux], flush=True)
wavs = []
with httpx.Client(timeout=300) as c:
    for x in morceaux:
        r = c.post(url + "/tts", json={"texte": x, "langue": "ma", "pas_flow": 10}, headers=h)
        assert r.status_code == 200 and r.content.startswith(b"RIFF"), (r.status_code, r.text[:120])
        wavs.append(r.content)
        print("morceau ok", r.headers.get("X-Duree-Ms"), "ms", flush=True)
with wave.open(io.BytesIO(wavs[0])) as w0:
    p = w0.getparams()
out = f"{dossier}/mixed/{ident}.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(p.nchannels); w.setsampwidth(p.sampwidth); w.setframerate(p.framerate)
    for i, b in enumerate(wavs):
        if i:
            w.writeframes(b"\0" * int(0.3 * p.framerate) * p.sampwidth * p.nchannels)
        with wave.open(io.BytesIO(b)) as wi:
            w.writeframes(wi.readframes(wi.getnframes()))
print("écrit", out)
