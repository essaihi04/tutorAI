"""Pose les pistes darija produites par Kaggle dans le cours exemple (sans base)."""
import hashlib
import json
import shutil
import sys
import wave
from pathlib import Path

SORTIE = Path(sys.argv[1])
VERSION = int(sys.argv[2])   # à augmenter à chaque régénération (le navigateur ne rejoue pas une ancienne piste)
AT = Path(r".")
COURS = sys.argv[3] if len(sys.argv) > 3 else "phys_ch1_waves_exemple"   # 3e argument : un autre cours (10 novembre 2026)
MANIFESTE = AT / f"backend/data/courses/{COURS}.json"
DEST = AT / f"frontend/public/media/audio/courses/{COURS}/mixed"

m = json.loads(MANIFESTE.read_text(encoding="utf-8"))
produits = {r["id"]: r for r in json.loads(next(SORTIE.rglob("cours.json")).read_text(encoding="utf-8"))}
DEST.mkdir(parents=True, exist_ok=True)
poses, manquants = 0, []
for a in m["activities"]:
    for s in a["slides"]:
        texte = (s.get("speech_text") or {}).get("mixed", "").strip()
        h = hashlib.sha256(texte.encode("utf-8")).hexdigest()
        p = produits.get(s["id"])
        wav = next(SORTIE.rglob(f"{s['id']}.wav"), None)
        if not p or not wav or p["hash"] != h:
            manquants.append(s["id"]); continue
        cible = DEST / f"{s['id']}_v{VERSION}.wav"
        shutil.copyfile(wav, cible)
        with wave.open(str(cible)) as w:
            ms = round(w.getnframes() / w.getframerate() * 1000)
        s["audio"] = {"mixed": {"url": f"/media/audio/courses/{COURS}/mixed/{cible.name}",
                                "duration_ms": ms, "version": VERSION, "speech_hash": h, "status": "published"}}
        poses += 1
        print(f"{s['id']:24s} {ms / 1000:5.1f} s")
MANIFESTE.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(poses, "pistes posées ; manquantes :", manquants)
