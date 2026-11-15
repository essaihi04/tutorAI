"""Réveille le kernel d'essai du compte 2 et génère UNE voix de diapositive en morceaux d'environ 300 caractères
(le tunnel coupe au-delà de ~100 s de calcul). Usage (VPS, env du compte 2 comme lancer_compte2.sh) :
  python voix_unique_compte2.py DOSSIER ID"""
import io, json, os, re, sys, wave

sys.path.insert(0, "/opt/moalim/backend")
import app.services.kaggle_tts as K

PROPRIETAIRE = os.environ.get("PROPRIETAIRE", "ferdaous04")
_construire = K.construire_kernel


def construire_kernel(dossier, *a, **k):
    d = _construire(dossier, *a, **k)
    p = dossier / "kernel-metadata.json"
    meta = json.loads(p.read_text(encoding="utf-8"))
    u = K.settings.kaggle_username
    meta["kernel_sources"] = [s.replace(f"{u}/", f"{PROPRIETAIRE}/", 1) for s in meta["kernel_sources"]]
    p.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return d


K.construire_kernel = construire_kernel
import httpx
from scripts.kaggle_tts import _reveiller_essai

dossier, ident = sys.argv[1:3]
m = json.load(open(f"{dossier}/cours.json", encoding="utf-8"))
texte = next(s for a in m["activities"] for s in a["slides"] if s["id"] == ident)["speech_text"]["mixed"].strip()
coupes = [mt.end() for mt in re.finditer(r"[.!?؟]\s+", texte)]
n = max(2, -(-len(texte) // 320))
bornes = sorted({min(coupes, key=lambda c: abs(c - len(texte) * k / n)) for k in range(1, n)})
morceaux = [texte[a:b].strip() for a, b in zip([0] + bornes, bornes + [len(texte)])]
print(len(texte), "caractères ->", [len(x) for x in morceaux], flush=True)

reveil = _reveiller_essai()
assert reveil, "kernel pas prêt"
url, jeton, _ = reveil
h = {"Authorization": "Bearer " + jeton}
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
print("écrit", out, flush=True)
