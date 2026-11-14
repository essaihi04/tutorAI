"""Pose dans les cours EN LIGNE les voix Bodi des réactions déjà générées par le lot du VPS (14 novembre 2026).

    python -X utf8 scripts/voix/poser_en_ligne.py --compter          # combien de pistes muettes, combien prêtes
    python -X utf8 scripts/voix/poser_en_ligne.py 12 [deck…]         # pose (MP3 *_v<V>.mp3) et écrit le cours

Sans voix posée, une réaction (« bravo », « pas tout à fait »…) est demandée à la voix en direct (GPU Kaggle) ;
quand le GPU dort ou démarre, l'élève n'entend rien. Même recherche que attente_poser.py (att_<deck>/, <deck>/,
_observations/, hash du texte identique), mais sur backend/data/courses/<deck>.json.
"""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pistes_cours import pistes

AT = Path(__file__).resolve().parents[2]
PUB = AT / "frontend/public"
COURS = AT / "backend/data/courses"
R = "/srv/corpus_v4/voix_lot"
S = Path(tempfile.gettempdir()) / "moalim-voix-en-ligne"
S.mkdir(exist_ok=True)
H = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()


def ssh(cmd, entree=None):
    return subprocess.run(["ssh", "moalim-vps", cmd], input=entree, capture_output=True)


def index_vps(deck):
    code = f"""
import json,os
R="{R}"; out={{}}
for dossier in ("att_{deck}","{deck}","_observations"):
    for sous in ("mixed","reponses","demos"):
        f=os.path.join(R,dossier,sous,"cours.json")
        if not os.path.isfile(f): continue
        for e in json.load(open(f,encoding="utf-8")):
            k=sous+"/"+e["id"]
            if k not in out and os.path.isfile(os.path.join(R,dossier,sous,e["id"]+".wav")): out[k]=[dossier,e["hash"]]
print(json.dumps(out))"""
    r = ssh("python3 -", code.encode())
    return json.loads(r.stdout.decode() or "{}")


def a_voix(d, i, poser, diapos, t):
    if d == "mixed":
        a = (diapos[i].get("audio") or {}).get("mixed") or {}
        return bool(a.get("url") and a.get("speech_hash") == H(t))
    cell = next((c.cell_contents for c in (poser.__closure__ or ()) if isinstance(c.cell_contents, dict)), {})
    return bool(cell.get("enonce_audio" if i.startswith("enonce_") else "audio"))


def decks_en_ligne():
    return sorted(p.stem for p in COURS.glob("*_ch*_*.json") if "_course_v1" not in p.name and "_script_" not in p.name)


def main():
    compter = "--compter" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--compter"]
    V = None if compter else int(args.pop(0))
    total = [0, 0, 0]
    for deck in args or decks_en_ligne():
        p = COURS / f"{deck}.json"
        m = json.loads(p.read_text(encoding="utf-8"))
        diapos = {s["id"]: s for a in m["activities"] for s in a["slides"]}
        idx = index_vps(deck)
        muettes, pretes = [], []
        for d, i, t, poser in pistes(m):
            if a_voix(d, i, poser, diapos, t):
                continue
            k = f"{d}/{i}"
            muettes.append(k)
            if k in idx and idx[k][1] == H(t):
                pretes.append((d, i, t, idx[k][0], poser))
        total[0] += len(muettes); total[1] += len(pretes)
        if compter:
            print(f"{deck[:48]:48s} muettes {len(muettes):4d}  prêtes sur le VPS {len(pretes):4d}")
            continue
        if pretes:
            T = Path(tempfile.mkdtemp(dir=S))
            liste = "\n".join(f"{dos}/{d}/{i}.wav" for d, i, _, dos, _ in pretes)
            t = ssh(f"cd {R} && tar -cf - -T -", liste.encode())
            subprocess.run(["tar", "-xf", "-", "-C", str(T)], input=t.stdout, check=True)
            for d, i, texte, dos, poser in pretes:
                wav = T / dos / d / f"{i}.wav"
                dest = PUB / f"media/audio/courses/{deck}/{d}/{i}_v{V}.mp3"
                dest.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1", "-codec:a",
                                "libmp3lame", "-q:a", "5", str(dest)], check=True)
                ms = int(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                               "csv=p=0", str(dest)], capture_output=True, text=True).stdout.strip() or 0) * 1000)
                poser(f"/media/audio/courses/{deck}/{d}/{i}_v{V}.mp3", ms, H(texte), V)
                total[2] += 1
            subprocess.run(["rm", "-rf", str(T)])
            p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"{deck} : {len(pretes)} posées, {len(muettes) - len(pretes)} encore muettes", flush=True)
    print(f"TOTAL : {total[0]} pistes muettes, {total[1]} prêtes sur le VPS" + ("" if compter else f", {total[2]} posées"))


if __name__ == "__main__":
    main()
