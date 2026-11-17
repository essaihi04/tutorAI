"""Pose dans les cours des voix refaites alors que leur texte n'a pas changé (skill prononciation, 16 novembre 2026).
poser_en_ligne.py ne pose que les pistes muettes (texte changé) ; une voix refaite pour une règle de prononciation,
une boucle ou une fin coupée garde le même texte, donc le même hash : on la pose ici avec une nouvelle version.

Usage (dans le dépôt) : python -X utf8 scripts/voix/poser_refaites.py VERSION CLE [CLE ...]
  CLE : deck/type/id (type : mixed, reponses, demos) ; le WAV est pris sur le VPS dans
        /srv/corpus_v4/voix_lot/att_<deck>/<type>/<id>.wav et doit porter dans cours.json le hash du texte actuel."""
import collections, hashlib, json, subprocess, sys, tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from pistes_cours import pistes

R = "/srv/corpus_v4/voix_lot"
COURS = ICI.parents[1] / "backend/data/courses"
PUB = ICI.parents[1] / "frontend/public"
H = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()
V = int(sys.argv[1])
cles = sys.argv[2:]
par_deck = collections.defaultdict(list)
for k in cles:
    deck, typ, i = k.split("/")
    par_deck[deck].append((typ, i))

T = Path(tempfile.mkdtemp())
liste = "\n".join(f"att_{d}/{t}/{i}.wav\natt_{d}/{t}/cours.json" for d, l in par_deck.items() for t, i in l)
tar = subprocess.run(["ssh", "moalim-vps", f"cd {R} && sort -u | tar -cf - -T -"], input=liste.encode(), capture_output=True)
subprocess.run(["tar", "-xf", "-", "-C", str(T)], input=tar.stdout, check=True)
posees, refus = 0, []
for deck, l in par_deck.items():
    p = COURS / f"{deck}.json"
    m = json.loads(p.read_text(encoding="utf-8"))
    voulues = set(l)
    for typ, i, texte, poser in pistes(m):
        if (typ, i) not in voulues:
            continue
        voulues.discard((typ, i))
        wav = T / f"att_{deck}" / typ / f"{i}.wav"
        idx = {e["id"]: e["hash"] for e in json.loads((wav.parent / "cours.json").read_text(encoding="utf-8"))}
        if not wav.is_file() or idx.get(i) != H(texte):
            refus.append(f"{deck}/{typ}/{i} (wav absent ou texte changé)")
            continue
        dest = PUB / f"media/audio/courses/{deck}/{typ}/{i}_v{V}.mp3"
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1", "-codec:a", "libmp3lame",
                        "-q:a", "5", str(dest)], check=True)
        ms = int(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                       str(dest)], capture_output=True, text=True).stdout.strip() or 0) * 1000)
        poser(f"/media/audio/courses/{deck}/{typ}/{i}_v{V}.mp3", ms, H(texte), V)
        posees += 1
    refus += [f"{deck}/{t}/{i} (piste introuvable dans le cours)" for t, i in voulues]
    p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
subprocess.run(["rm", "-rf", str(T)])
print(posees, "posées en v%d" % V)
for r in refus:
    print("REFUS", r)
