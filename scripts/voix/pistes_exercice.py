"""Les pistes à dire d'un EXERCICE (partie « Exercices », 22 novembre 2026 — skill `exercices`), et leur pose.

Chaque piste : (dossier, id, texte, poser(url, duree_ms, hash, version)), comme `pistes_cours.pistes` :
  enonce      : l'énoncé lu (intro_dit -> intro_audio) et chaque question (texte_dit -> texte_audio)
  aides       : les aides du tuteur (aides[k].dit -> aides[k].audio)
  corrections : la correction dite (correction.parole -> correction.audio)
  + l'exercice semblable (préfixe « b_ ») et les diapositives d'explication et de version facile (format des cours :
    mixed, reponses, demos, énoncés, associations — mêmes ids que dans un cours).

Usage :
  python -X utf8 scripts/voix/pistes_exercice.py liste EXERCICE.json [...]       -> liste du lot sans tunnel (stdout, JSON)
  python -X utf8 scripts/voix/pistes_exercice.py poser VERSION EXERCICE.json [...] -> WAV du VPS (att_<id>/<dossier>/<piste>)
        convertis en MP3 dans frontend/public/media/audio/exercices/<id>/<dossier>/, champs audio posés dans le JSON.
"""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pistes_cours import pistes as pistes_cours  # noqa: E402

R = "/srv/corpus_v4/voix_lot"
H = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()  # noqa: E731


def _champ(obj, cle):
    def f(url, ms, h, v):
        obj[cle] = url
    return f


def _enonce(e, pre):
    en = e.get("enonce") or {}
    if (en.get("intro_dit") or "").strip():
        yield ("enonce", f"{pre}intro", en["intro_dit"].strip(), _champ(en, "intro_audio"))
    for q in en.get("questions") or []:
        if (q.get("texte_dit") or "").strip():
            yield ("enonce", f"{pre}q{q['id']}", q["texte_dit"].strip(), _champ(q, "texte_audio"))
        for k, a in enumerate(q.get("aides") or []):
            if (a.get("dit") or "").strip():
                yield ("aides", f"{pre}q{q['id']}_a{k + 1}", a["dit"].strip(), _champ(a, "audio"))
        c = q.get("correction") or {}
        if (c.get("parole") or "").strip():
            yield ("corrections", f"{pre}q{q['id']}", c["parole"].strip(), _champ(c, "audio"))


def pistes(e):
    yield from _enonce(e, "")
    yield from _enonce(e.get("similaire") or {}, "b_")
    for deck in ("explication", "facile"):
        yield from pistes_cours(e.get(deck) or {"activities": []})


def _liste(fichiers):
    out = []
    for f in fichiers:
        e = json.loads(Path(f).read_text(encoding="utf-8"))
        for dossier, i, texte, _ in pistes(e):
            out.append({"cle": f"{e['id']}/{dossier}/{i}", "texte": texte, "cours": e["id"]})
    return out


def _poser(v, fichiers):
    racine = Path(__file__).resolve().parents[2] / "frontend" / "public"
    for f in fichiers:
        p = Path(f)
        e = json.loads(p.read_text(encoding="utf-8"))
        ex = e["id"]
        voulues = list(pistes(e))
        T = Path(tempfile.mkdtemp())
        liste = "\n".join(f"att_{ex}/{d}/{i}.wav\natt_{ex}/{d}/cours.json" for d, i, _, _ in voulues)
        tar = subprocess.run(["ssh", "moalim-vps", f"cd {R} && sort -u | tar -cf - -T - 2>/dev/null"], input=liste.encode(), capture_output=True)
        subprocess.run(["tar", "-xf", "-", "-C", str(T)], input=tar.stdout)
        posees, refus = 0, []
        for d, i, texte, poser in voulues:
            wav = T / f"att_{ex}" / d / f"{i}.wav"
            idx_f = wav.parent / "cours.json"
            idx = {x["id"]: x["hash"] for x in json.loads(idx_f.read_text(encoding="utf-8"))} if idx_f.is_file() else {}
            if not wav.is_file() or idx.get(i) != H(texte):
                refus.append(f"{d}/{i}")
                continue
            rel = f"media/audio/exercices/{ex}/{d}/{i}_v{v}.mp3"
            dest = racine / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1", "-codec:a", "libmp3lame", "-q:a", "5", str(dest)], check=True)
            ms = int(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dest)],
                                          capture_output=True, text=True).stdout.strip() or 0) * 1000)
            poser("/" + rel, ms, H(texte), v)
            posees += 1
        p.write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        subprocess.run(["rm", "-rf", str(T)])
        print(ex, ":", posees, "posées en v%d" % v, "|", len(refus), "sans voix", refus[:8])


if __name__ == "__main__":
    if sys.argv[1] == "liste":
        print(json.dumps(_liste(sys.argv[2:]), ensure_ascii=False))
    elif sys.argv[1] == "poser":
        _poser(int(sys.argv[2]), sys.argv[3:])
