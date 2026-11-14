"""Pose les voix Bodi dans les cours en attente (14 novembre 2026).
python -X utf8 poser.py <version> [deck…]
Pour chaque piste sans voix de backend/data/courses/en_attente/<deck>.json, cherche le WAV prêt sur le VPS, dans cet
ordre : att_<deck>/, <deck>/ (dossier du cours en ligne), _observations/. Le hash du texte doit être le même que celui
du dossier (cours.json de chaque sous-dossier), sinon la piste n'est pas posée. MP3 dans
frontend/public/media/audio/courses/<deck>/<sous-dossier>/<id>_v<V>.mp3. Écrit le cours en attente en place et dit ce
qui manque encore."""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pistes_cours import pistes

S = Path(__import__("tempfile").gettempdir()) / "moalim-voix-attente"   # sorties hors du dépôt
S.mkdir(exist_ok=True)
AT = Path(__file__).resolve().parents[2]
PUB = AT / "frontend/public"
R = "/srv/corpus_v4/voix_lot"
V = int(sys.argv[1])
H = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()
decks = sys.argv[2:] or sorted(p.stem for p in (AT / "backend/data/courses/en_attente").glob("*.json"))


def ssh(cmd, entree=None):
    return subprocess.run(["ssh", "moalim-vps", cmd], input=entree, capture_output=True)


def index_vps(deck):
    """{(sous, id): (dossier, hash)} des WAV prêts, att_ d'abord."""
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


def obs_cibles(m):
    for a in m.get("activities") or []:
        for s in a["slides"]:
            o = (s.get("concentration") or {}).get("observation")
            if not o:
                continue
            b = f"enonce_obs_{s['id']}"
            if not o.get("enonce_audio") and (o.get("enonce_dit") or o.get("enonce")):
                yield f"{b}_q", (o.get("enonce_dit") or o["enonce"]).strip(), o, "enonce_audio"
            for i, x in enumerate(o.get("indices") or []):
                if not x.get("audio") and (x.get("dit") or x.get("texte")):
                    yield f"{b}_i{i}", (x.get("dit") or x["texte"]).strip(), x, "audio"
            for i, x in enumerate(o.get("retours") or []):
                if not x.get("audio") and x.get("parole"):
                    yield f"{b}_r{i}", x["parole"].strip(), x, "audio"
            so = o.get("solution") or {}
            if not so.get("audio") and so.get("parole"):
                yield f"{b}_s", so["parole"].strip(), so, "audio"


def deja_en_ligne(deck):
    """{(sous/id): (hash, url)} des pistes déjà posées dans le cours en ligne : réutilisées telles quelles (disque)."""
    lp = AT / "backend/data/courses" / f"{deck}.json"
    if not lp.exists():
        return {}
    ml = json.loads(lp.read_text(encoding="utf-8"))
    dl = {s["id"]: s for a in ml["activities"] for s in a["slides"]}
    out = {}
    for d, i, t, poser in pistes(ml):
        if d == "mixed":
            a = (dl[i].get("audio") or {}).get("mixed") or {}
            if a.get("url") and a.get("speech_hash") == H(t):
                out[f"{d}/{i}"] = (H(t), a["url"], a.get("duration_ms", 0))
            continue
        cell = next((c.cell_contents for c in (poser.__closure__ or ()) if isinstance(c.cell_contents, dict)), {})
        url = cell.get("enonce_audio" if i.startswith("enonce_") else "audio")
        if url and (PUB / url.lstrip("/")).exists():
            out[f"{d}/{i}"] = (H(t), url, 0)
    for i, t, obj, cle in obs_cibles_toutes(ml):
        url = obj.get(cle)
        if url and (PUB / url.lstrip("/")).exists():
            out[f"reponses/{i}"] = (H(t), url, 0)
    return out


def obs_cibles_toutes(m):
    """Comme obs_cibles, mais aussi les champs qui ont déjà une voix."""
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


for deck in decks:
    p = AT / "backend/data/courses/en_attente" / f"{deck}.json"
    m = json.loads(p.read_text(encoding="utf-8"))
    idx = index_vps(deck)
    en_ligne = deja_en_ligne(deck)
    repris = 0
    diapos = {s["id"]: s for a in m["activities"] for s in a["slides"]}
    a_poser, manquent = [], []
    for d, i, t, poser in pistes(m):
        if d == "mixed":
            a = (diapos[i].get("audio") or {}).get("mixed") or {}
            if a.get("url") and a.get("speech_hash") == H(t):
                continue
        else:
            cell = next((c.cell_contents for c in (poser.__closure__ or ()) if isinstance(c.cell_contents, dict)), {})
            if cell.get("enonce_audio" if i.startswith("enonce_") else "audio"):
                continue
        k = f"{d}/{i}"
        if k in en_ligne and en_ligne[k][0] == H(t):
            poser(en_ligne[k][1], en_ligne[k][2], H(t), V); repris += 1
        elif k in idx and idx[k][1] == H(t):
            a_poser.append((d, i, t, idx[k][0], poser))
        else:
            manquent.append(k)
    for i, t, obj, cle in obs_cibles(m):
        k = f"reponses/{i}"
        if k in en_ligne and en_ligne[k][0] == H(t):
            obj[cle] = en_ligne[k][1]; repris += 1
        elif k in idx and idx[k][1] == H(t):
            a_poser.append(("reponses", i, t, idx[k][0], (lambda o, c: (lambda url, ms, h, v: o.__setitem__(c, url)))(obj, cle)))
        else:
            manquent.append(k)
    if a_poser:
        T = Path(tempfile.mkdtemp(dir=S))
        liste = "\n".join(f"{dos}/{d}/{i}.wav" for d, i, _, dos, _ in a_poser)
        t = ssh(f"cd {R} && tar -cf - -T -", liste.encode())
        subprocess.run(["tar", "-xf", "-", "-C", str(T)], input=t.stdout, check=True)
        for d, i, texte, dos, poser in a_poser:
            wav = T / dos / d / f"{i}.wav"
            dest = PUB / f"media/audio/courses/{deck}/{d}/{i}_v{V}.mp3"
            dest.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1", "-codec:a", "libmp3lame", "-q:a", "5", str(dest)], check=True)
            ms = int(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dest)],
                                          capture_output=True, text=True).stdout.strip() or 0) * 1000)
            poser(f"/media/audio/courses/{deck}/{d}/{i}_v{V}.mp3", ms, H(texte), V)
        subprocess.run(["rm", "-rf", str(T)])
    p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{deck} : {repris} reprises du cours en ligne, {len(a_poser)} nouvelles posées, {len(manquent)} manquent encore")
