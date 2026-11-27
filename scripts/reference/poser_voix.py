"""Pose les voix Bodi du cours de référence SVT (27/11/2026) : `python -I -X utf8 scripts/reference/poser_voix.py [version]`.

Les WAV générés (Colab, lots refsvt1..7) et vérifiés par MoulSot sont sur le VPS dans
/srv/corpus_v4/voix_lot/att_svt_ch1_reference_consommation_mo/<dossier>/<id>.wav, avec un cours.json par dossier
(id + hash du texte). Comme `scripts/voix/attente_poser.py`, mais pour ce cours (pas « en attente ») et avec le dossier
`observations` (énoncés, indices, retours et solutions des observations guidées). Une piste n'est posée que si le hash
de son texte est celui du WAV : un texte changé depuis la génération reste sans voix et est listé.
MP3 : frontend/public/media/audio/courses/<deck>/<dossier>/<id>_v<V>.mp3 ; le cours est réécrit en place."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AT / "scripts/voix"))
from pistes_cours import pistes  # noqa: E402

DECK = "svt_ch1_reference_consommation_mo"
R = "/srv/corpus_v4/voix_lot"
DOS = f"att_{DECK}"
V = int(sys.argv[1]) if len(sys.argv) > 1 else 1
PUB = AT / "frontend/public"
P = AT / "backend/data/courses" / f"{DECK}.json"
H = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()  # noqa: E731


def ssh(cmd, entree=None):
    return subprocess.run(["ssh", "moalim-vps", cmd], input=entree, capture_output=True)


def index_vps():
    """{dossier/id: hash} des WAV prêts."""
    code = f"""
import json,os
base=os.path.join("{R}","{DOS}"); out={{}}
for sous in ("mixed","reponses","observations","demos"):
    f=os.path.join(base,sous,"cours.json")
    if not os.path.isfile(f): continue
    for e in json.load(open(f,encoding="utf-8")):
        if os.path.isfile(os.path.join(base,sous,e["id"]+".wav")): out[sous+"/"+e["id"]]=e["hash"]
print(json.dumps(out))"""
    r = ssh("python3 -", code.encode())
    return json.loads(r.stdout.decode() or "{}")


def observations(m):
    """Les pistes des observations guidées : (id, texte, objet, clé où poser l'url)."""
    for a in m.get("activities") or []:
        for s in a["slides"]:
            o = (s.get("concentration") or {}).get("observation")
            if not o:
                continue
            b = f"enonce_obs_{s['id']}"
            if o.get("enonce_dit") or o.get("enonce"):
                yield f"{b}_q", (o.get("enonce_dit") or o["enonce"]).strip(), o, "enonce_audio"
            for i, x in enumerate(o.get("indices") or []):
                if x.get("dit") or x.get("texte"):
                    yield f"{b}_i{i}", (x.get("dit") or x["texte"]).strip(), x, "audio"
            for i, x in enumerate(o.get("retours") or []):
                if x.get("parole"):
                    yield f"{b}_r{i}", x["parole"].strip(), x, "audio"
            so = o.get("solution") or {}
            if so.get("parole"):
                yield f"{b}_s", so["parole"].strip(), so, "audio"


def main():
    m = json.loads(P.read_text(encoding="utf-8"))
    idx = index_vps()
    cibles = [(d, i, t, poser) for d, i, t, poser in pistes(m)]
    cibles += [("observations", i, t, (lambda o, c: (lambda url, ms, h, v: o.__setitem__(c, url)))(o, c)) for i, t, o, c in observations(m)]
    a_poser, manquent, changees = [], [], []
    for d, i, t, poser in cibles:
        k = f"{d}/{i}"
        if k not in idx:
            manquent.append(k)
        elif idx[k] != H(t):
            changees.append(k)
        else:
            a_poser.append((d, i, t, poser))
    T = Path(tempfile.mkdtemp(prefix="voix-ref-"))
    try:
        for n in range(0, len(a_poser), 40):        # par paquets : peu de place sur le disque C:
            paquet = a_poser[n:n + 40]
            liste = "\n".join(f"{DOS}/{d}/{i}.wav" for d, i, _, _ in paquet)
            t = ssh(f"cd {R} && tar -cf - -T -", liste.encode())
            subprocess.run(["tar", "-xf", "-", "-C", str(T)], input=t.stdout, check=True)
            for d, i, texte, poser in paquet:
                wav = T / DOS / d / f"{i}.wav"
                dest = PUB / f"media/audio/courses/{DECK}/{d}/{i}_v{V}.mp3"
                dest.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1", "-codec:a", "libmp3lame", "-q:a", "5", str(dest)], check=True)
                ms = int(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dest)],
                                              capture_output=True, text=True).stdout.strip() or 0) * 1000)
                poser(f"/media/audio/courses/{DECK}/{d}/{i}_v{V}.mp3", ms, H(texte), V)
                wav.unlink()
    finally:
        shutil.rmtree(T, ignore_errors=True)
    P.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{DECK} : {len(a_poser)} posées sur {len(cibles)} pistes, {len(manquent)} pas encore générées, {len(changees)} au texte changé")
    for k in changees:
        print("  texte changé :", k)


if __name__ == "__main__":
    main()
